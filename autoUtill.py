# autoUtill.py
import time, os;
from pywinauto.application import Application

def retry_function(retry_times=3, delay=2):
    """
    一个装饰器函数，用于实现重试机制。
    :param retry_times: 重试次数
    :param delay: 每次重试之间的等待时间（秒）
    :return: 被装饰的函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retry_times:
                try:
                    return func(*args, **kwargs)  # 尝试执行被装饰的函数
                except Exception as e:
                    print(f"尝试 {attempts + 1} 失败，错误信息：{e}")
                    attempts += 1
                    if attempts < retry_times:
                        print(f"等待 {delay} 秒后重试...")
                        time.sleep(delay)  # 等待一段时间后再次尝试
                    else:
                        raise  # 所有重试次数用完，重新抛出异常
        return wrapper
    return decorator

retry_times = 3;
delay = 5;

@retry_function(retry_times, delay)
def clickComponent(app, title, name, parent=None):
    if(parent == None):
        rootWindows = getComponentByTitle(app, title);
    else:
        rootWindows = parent;
    rootWindows.set_focus();
    rootWindows[name].wait('visible', timeout=20, retry_interval=5)
    rootWindows[name].click_input();
    time.sleep(0.5);

@retry_function(retry_times, delay)
def setEditComponent(app, title, name, contentText, parent=None):
    if (parent == None):
        rootWindows = getComponentByTitle(app, title);
    else:
        rootWindows = parent;
    rootWindows.set_focus();
    rootWindows[name].wait('visible', timeout=10, retry_interval=1)
    textEdit = rootWindows[name];
    textEdit.set_edit_text("");
    textEdit.set_edit_text(contentText);
    time.sleep(0.5);

@retry_function(retry_times, delay)
def getRectangleByTitle(app, title, name, parent=None):
    if (parent == None):
        rootWindows = getComponentByTitle(app, title);
    else:
        rootWindows = parent;
    rootWindows[name].wait('visible', timeout=10, retry_interval=1)
    return (rootWindows[name]).rectangle();
@retry_function(retry_times, delay)
def getChildComponentByTitleAndAutoID(app, title, autoId):
    app.window(title=title, auto_id=autoId).wait('visible', timeout=600, retry_interval=20)
    return app.window(title=title, auto_id=autoId);

@retry_function(retry_times, delay)
def getComponentByTitle(app, title):
    app.window(title=title).wait('visible', timeout=60, retry_interval=5)
    return app.window(title=title);

@retry_function(retry_times, delay)
def getComponentByTitleAndAutoID(parent, title, autoId, timeout=20, retry_interval=5):
    parent.window(title=title, auto_id=autoId).wait('visible', timeout=timeout, retry_interval=retry_interval)
    return parent.window(title=title, auto_id=autoId);

@retry_function(retry_times, delay)
def getAppByTitle(title, type="uia"):
    app=Application(backend=type).connect(title=title);
    # app.window(title=title).wait('visible', timeout=30, retry_interval=5);
    return app;

@retry_function(retry_times, delay)
def waitOrWaitNotComponent(parent, name, type=0, timeout=10, retry_interval=1):
    if type == 0:
        parent[name].wait('visible', timeout=timeout, retry_interval=retry_interval);
    else:
        parent[name].wait_not('visible', timeout=timeout, retry_interval=retry_interval);

@retry_function(retry_times, delay)
def getApp(window_title, executable=r'D:\JianyingPro\JianyingPro.exe', backend="uia", timeout=5):
    # 尝试连接到已经打开的应用程序
    try:
        app = Application(backend=backend).connect(title=window_title, timeout=timeout)
        print("应用程序已经打开并连接成功。")
    except Exception as e:
        print("无法连接到应用程序，可能是因为它没有打开或者窗口标题不正确。尝试启动应用程序...")
        try:
            # 启动应用程序
            os.system(f"start {executable}");
            time.sleep(5);
            app = Application(backend=backend).connect(title=window_title, timeout=timeout)
            print("应用程序已成功启动。")
        except Exception as e:
            print("无法启动应用程序。", e)
    finally:
        return app;