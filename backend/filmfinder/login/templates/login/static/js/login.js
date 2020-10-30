const username = document.getElementById("username");
const password = document.getElementById("password");
const login = document.getElementById("login");

const Invalidusername = document.getElementById("Invalidusername");
const Invalidpassword = document.getElementById("Invalidpassword");
const isValidUserName = () => {
  const pattern = /^.+\@.+\..+$/;
  return pattern.test(username.value);
};

const isValidPassword = () => {
  const pattern = /^.{6,20}$/;
  return pattern.test(password.value);
};

const checkCanSubmit = () => {
  if (isValidPassword() && isValidUserName()) {
    login.removeAttribute("disabled");
  } else {
    login.setAttribute("disabled", "disabled");
  }
};
username.addEventListener("keyup", checkCanSubmit);
password.addEventListener("keyup", checkCanSubmit);

username.addEventListener("blur", () => {
  if (!isValidUserName()) {
    Invalidusername.style.visibility = "visible";
  }
});

username.addEventListener("focus", () => {
  Invalidusername.style.visibility = "hidden";
});

password.addEventListener("blur", () => {
  if (!isValidPassword()) {
    Invalidpassword.style.visibility = "visible";
  }
});

password.addEventListener("focus", () => {
  Invalidpassword.style.visibility = "hidden";
});


var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
        httpRequest.open('GET', 'url', true);//第二步：打开连接  将请求参数写在url中  ps:"./Ptest.php?name=test&nameone=testone"
        httpRequest.send();//第三步：发送请求  将请求参数写在URL中
        /**
         * 获取数据后的处理程序
         */
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState == 4 && httpRequest.status == 200) {
                var json = httpRequest.responseText;//获取到json字符串，还需解析
                console.log(json);
            }
        };

var httpRequest = new XMLHttpRequest();//第一步：创建需要的对象
httpRequest.open('POST', 'url', true); //第二步：打开连接
httpRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
httpRequest.send('name=teswe&ee=ef');//发送请求 将情头体写在send中
/**
 * 获取数据后的处理程序
 */
httpRequest.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
    if (httpRequest.readyState == 4 && httpRequest.status == 200) {//验证请求是否发送成功
        var json = httpRequest.responseText;//获取到服务端返回的数据
        console.log(json);
    }
};


var httpRequest = new XMLHttpRequest();//第一步：创建需要的对象
httpRequest.open('POST', 'url', true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
httpRequest.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）var obj = { name: 'zhansgan', age: 18 };
httpRequest.send(JSON.stringify(obj));//发送请求 将json写入send中
/**
 * 获取数据后的处理程序
 */
httpRequest.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
    if (httpRequest.readyState == 4 && httpRequest.status == 200) {//验证请求是否发送成功
        var json = httpRequest.responseText;//获取到服务端返回的数据
        console.log(json);
    }
};
