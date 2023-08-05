from typing import Optional, List, Any, Dict, Tuple
import asyncio
import contextlib
import enum
import pathlib
import queue
import shlex
import threading

from wcpan.drive.core.types import Node
from wcpan.drive.core.drive import DriveFactory, Drive

from .util import print_as_yaml


class TokenType(enum.Enum):
    Global = enum.auto()
    Path = enum.auto()


class ShellContext(object):

    def __init__(self, drive: 'DriveProxy', home_node: Node) -> None:
        self._drive = drive
        self._home = home_node
        self._cwd = home_node
        self._actions = {
            'help': self._help,
            'ls': self._list,
            'cd': self._chdir,
            'mkdir': self._mkdir,
            'sync': self._sync,
            'pwd': self._pwd,
            'find': self._find,
            'info': self._info,
            'hash': self._hash,
            'id_to_path': self._id_to_path,
            'path_to_id': self._path_to_id,
        }
        self._cache = ChildrenCache(drive)

    def get_prompt(self) -> str:
        if not self._cwd.name:
            name = '/'
        else:
            name = self._cwd.name
        return f'{name} > '

    def complete(self, text: str, state: int) -> Optional[str]:
        import readline
        whole_text = readline.get_line_buffer()
        end_index = readline.get_endidx()
        type_, token = parse_completion(whole_text, end_index)

        if type_ == TokenType.Global:
            values = self._get_global(text)
        elif type_ == TokenType.Path:
            values = self._get_path(text, token)
        else:
            return None

        try:
            return values[state]
        except IndexError:
            return None

    def execute(self, line: str) -> None:
        cmd = shlex.split(line)

        if not cmd:
            return

        command = cmd[0]
        if command not in self._actions:
            print(f'unknown command {command}')
            return

        action = self._actions[command]
        try:
            action(*cmd[1:])
        except TypeError as e:
            print(e)

    def _get_global(self, prefix: str) -> List[str]:
        cmd = self._actions.keys()
        cmd = [c for c in cmd if c.startswith(prefix)]
        return cmd

    def _get_path(self, prefix: str, path: str) -> List[str]:
        children = self._cache.get(self._cwd, path)
        children = [c for c in children if c.startswith(prefix)]
        return children

    def _help(self) -> None:
        cmd = self._actions.keys()
        for c in cmd:
            print(c)

    def _list(self, src: str = None) -> None:
        if not src:
            node = self._cwd
        else:
            path = normalize_path(self._drive, self._cwd, src)
            node = self._drive.get_node_by_path(path)
            if not node:
                print(f'{src} not found')
                return

        children = self._drive.get_children(node)
        for child in children:
            print(child.name)

    def _chdir(self, src: str = None) -> None:
        if not src:
            self._cwd = self._home
            return

        path = normalize_path(self._drive, self._cwd, src)
        node = self._drive.get_node_by_path(path)
        if not node:
            print(f'unknown path {src}')
            return
        if not node.is_folder:
            print(f'{src} is not a folder')
            return

        self._cwd = node

    def _mkdir(self, src: str) -> None:
        if not src:
            print(f'invalid name')
            return

        self._drive.create_folder(self._cwd, src)

    def _sync(self) -> None:
        self._cache.reset()
        self._drive.sync()

    def _pwd(self) -> None:
        print(self._drive.get_path(self._cwd))

    def _find(self, src: str) -> None:
        rv = self._drive.search_by_regex(src)
        for [id_, path] in rv:
            print(f'{id_} - {path}')

    def _info(self, src: str) -> None:
        node = self._drive.get_node_by_id(src)
        if not node:
            print('null')
        else:
            print_as_yaml(node.to_dict())

    def _hash(self, *args) -> None:
        rv = self._drive.get_hash_list(self._cwd, args)
        for [path_or_id, hash_] in rv:
            print(f'{hash_} - {path_or_id}')

    def _id_to_path(self, src: str) -> None:
        node = self._drive.get_node_by_id(src)
        if not node:
            print(f'{src} not found')
            return
        path = self._drive.get_path(node)
        print(path)

    def _path_to_id(self, src: str) -> None:
        path = normalize_path(self._drive, self._cwd, src)
        node = self._drive.get_node_by_path(path)
        if not node:
            print(f'{src} not found')
            return
        print(node.id_)


class ChildrenCache(object):

    def __init__(self, drive: 'DriveProxy') -> None:
        self._drive = drive
        self._cache = {}

    def get(self, cwd: Node, src: str) -> List[str]:
        key = f'{cwd.id_}:{src}'
        if key in self._cache:
            return self._cache[key]

        path = normalize_path(self._drive, cwd, src)
        node = self._drive.get_node_by_path(path)
        if not node:
            parent_path = path.parent
            node = self._drive.get_node_by_path(parent_path)

        children = self._drive.get_children(node)
        self._cache[key] = [child.name for child in children]
        return self._cache[key]

    def reset(self) -> None:
        self._cache = {}


class DriveProxy(object):

    def __init__(self, factory: DriveFactory) -> None:
        self._factory = factory
        self._thread = threading.Thread(target=self._main)
        self._queue = queue.Queue()
        self._actions = {
            'sync': self._sync,
            'get_node_by_path': self._get_node_by_path,
            'get_path': self._get_path,
            'get_children': self._get_children,
            'search_by_regex': self._search_by_regex,
            'get_node_by_id': self._get_node_by_id,
            'get_hash_list': self._get_hash_list,
            'create_folder': self._create_folder,
        }

    def __enter__(self) -> 'DriveProxy':
        self._thread.start()
        return self

    def __exit__(self, et, ev, tb) -> bool:
        self._queue.put(None)
        self._queue.join()
        self._thread.join()

    def _main(self) -> None:
        assert_off_main_thread()

        asyncio.run(self._amain())

    async def _amain(self) -> None:
        assert_off_main_thread()

        async with self._factory() as drive:
            while True:
                task = self._queue.get()
                try:
                    if not task:
                        break

                    if task.action not in self._actions:
                        print(f'unknown action {task.action}')
                        return

                    action = self._actions[task.action]
                    await action(drive, task)
                except Exception as e:
                    print(e)
                finally:
                    if task:
                        with task as cv:
                            cv.notify()
                    self._queue.task_done()

    def sync(self) -> None:
        task = OffMainThreadTask(
            action='sync',
            args=(),
            kwargs={},
        )
        self._queue.put(task)
        with task as cv:
            cv.wait()

    async def _sync(self, drive: Drive, task: 'OffMainThreadTask') -> None:
        assert_off_main_thread()

        async for change in drive.sync():
            print(change)
        task.return_value = None

    def get_node_by_path(self, path: pathlib.PurePath) -> Optional[Node]:
        task = OffMainThreadTask(
            action='get_node_by_path',
            args=(path,),
            kwargs={},
        )
        self._queue.put(task)
        with task as cv:
            cv.wait()
        return task.return_value

    async def _get_node_by_path(self, drive: Drive, task: 'OffMainThreadTask') -> None:
        assert_off_main_thread()

        rv = await drive.get_node_by_path(*task.args, **task.kwargs)
        task.return_value = rv

    def get_path(self, node: Node) -> pathlib.PurePath:
        task = OffMainThreadTask(
            action='get_path',
            args=(node,),
            kwargs={},
        )
        self._queue.put(task)
        with task as cv:
            cv.wait()
        return task.return_value

    async def _get_path(self, drive: Drive, task: 'OffMainThreadTask') -> None:
        assert_off_main_thread()

        rv = await drive.get_path(*task.args, **task.kwargs)
        task.return_value = rv

    def get_children(self, node: Node) -> List[Node]:
        task = OffMainThreadTask(
            action='get_children',
            args=(node,),
            kwargs={},
        )
        self._queue.put(task)
        with task as cv:
            cv.wait()
        return task.return_value

    async def _get_children(self, drive: Drive, task: 'OffMainThreadTask') -> None:
        assert_off_main_thread()

        rv = await drive.get_children(*task.args, **task.kwargs)
        task.return_value = rv

    def search_by_regex(self, pattern: str) -> List[Tuple[str, str]]:
        task = OffMainThreadTask(
            action='search_by_regex',
            args=(pattern,),
            kwargs={},
        )
        self._queue.put(task)
        with task as cv:
            cv.wait()
        return task.return_value

    async def _search_by_regex(self, drive: Drive, task: 'OffMainThreadTask') -> None:
        assert_off_main_thread()

        node_list = await drive.find_nodes_by_regex(*task.args, **task.kwargs)
        path_list = [drive.get_path(node) for node in node_list]
        path_list = await asyncio.gather(*path_list)
        id_list = [node.id_ for node in node_list]
        rv = zip(id_list, path_list)
        task.return_value = list(rv)

    def get_node_by_id(self, id_: str) -> Optional[Node]:
        task = OffMainThreadTask(
            action='get_node_by_id',
            args=(id_,),
            kwargs={},
        )
        self._queue.put(task)
        with task as cv:
            cv.wait()
        return task.return_value

    async def _get_node_by_id(self, drive: Drive, task: 'OffMainThreadTask') -> None:
        assert_off_main_thread()

        rv = await drive.get_node_by_id(*task.args, **task.kwargs)
        task.return_value = rv

    def get_hash_list(self, cwd: Node, path_or_id_list: List[str]) -> List[Tuple[str, str]]:
        task = OffMainThreadTask(
            action='get_hash_list',
            args=(cwd, path_or_id_list,),
            kwargs={},
        )
        self._queue.put(task)
        with task as cv:
            cv.wait()
        return task.return_value

    async def _get_hash_list(self, drive: Drive, task: 'OffMainThreadTask') -> None:
        assert_off_main_thread()

        cwd = task.args[0]
        path_or_id_list = task.args[1]

        base_path = await drive.get_path(cwd)
        node_list = [
            get_node_by_path_or_id(drive, base_path, path_or_id)
            for path_or_id in path_or_id_list
        ]
        node_list = await asyncio.gather(*node_list)
        hash_list = [node.hash_ for node in node_list]
        rv = zip(path_or_id_list, hash_list)
        task.return_value = list(rv)

    def create_folder(self, node: Node, name: str) -> None:
        task = OffMainThreadTask(
            action='create_folder',
            args=(node, name),
            kwargs={},
        )
        self._queue.put(task)
        with task as cv:
            cv.wait()

    async def _create_folder(self, drive: Drive, task: 'OffMainThreadTask') -> None:
        assert_off_main_thread()

        rv = await drive.create_folder(*task.args, **task.kwargs)
        task.return_value = rv


class OffMainThreadTask(object):

    def __init__(self, action: str, args: Tuple[Any], kwargs=Dict[str, Any]) -> None:
        self._action = action
        self._args = args
        self._kwargs = kwargs
        self._done = threading.Condition()
        self._raii = None
        self.return_value = None

    def __enter__(self) -> threading.Condition:
        with contextlib.ExitStack() as stack:
            stack.enter_context(self._done)
            self._raii = stack.pop_all()
        return self._done

    def __exit__(self, et, ev, tb) -> bool:
        self._raii.close()

    @property
    def action(self) -> str:
        return self._action

    @property
    def args(self) -> Tuple[Any]:
        return self._args

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self._kwargs


def interact(factory: DriveFactory, home_node: Node) -> None:
    with DriveProxy(factory) as drive:
        context = ShellContext(drive, home_node)

        import readline
        readline.set_completer_delims('/ ')
        readline.set_completer(context.complete)
        readline.parse_and_bind('tab: complete')

        while True:
            prompt = context.get_prompt()
            try:
                line = input(prompt)
            except EOFError:
                break

            context.execute(line)

    # reset anchor
    print()


def resolve_path(
    from_: pathlib.PurePath,
    to: pathlib.PurePath,
) -> pathlib.PurePath:
    rv = from_
    for part in to.parts:
        if part == '.':
            continue
        elif part == '..':
            rv = rv.parent
        else:
            rv = rv / part
    return rv


def normalize_path(
    drive: DriveProxy,
    node: Node,
    string: str,
) -> pathlib.PurePath:
    path = pathlib.PurePath(string)
    if not path.is_absolute():
        current_path = drive.get_path(node)
        path = resolve_path(current_path, path)
    return path


def parse_completion(whole_text, end_index):
    lexer = shlex.shlex(whole_text, posix=True)
    lexer.whitespace_split = True

    cmd = []
    offset = 0

    while True:
        try:
            token = lexer.get_token()
        except ValueError:
            idx = whole_text.find(token, offset)
            assert idx >= 0
            offset = idx + len(token)
            cmd.append((idx, lexer.token))
            break

        if token == lexer.eof:
            break

        idx = whole_text.find(token, offset)
        assert idx >= 0
        offset = idx + len(token)
        cmd.append((idx, token))

    idx = None
    token = None
    token_list = [(idx, offset, token) for idx, (offset, token) in enumerate(cmd)]
    for idx, offset, token in reversed(token_list):
        if offset <= end_index:
            break

    if idx == 0:
        return TokenType.Global, token
    else:
        return TokenType.Path, token


def assert_off_main_thread():
    assert threading.current_thread() is not threading.main_thread()


async def get_node_by_path_or_id(
    drive: Drive,
    cwd: pathlib.PurePath,
    path_or_id: str,
) -> Node:
    node = await drive.get_node_by_id(path_or_id)
    if node:
        return node

    path = pathlib.PurePath(path_or_id)
    if path.is_absolute():
        node = await drive.get_node_by_path(path)
        return node

    path = resolve_path(cwd, path)
    node = await drive.get_node_by_path(path)
    return node
