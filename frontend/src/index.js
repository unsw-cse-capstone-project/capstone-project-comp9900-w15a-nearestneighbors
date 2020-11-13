import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import Login from './component/Login';
import Detail from './component/Detail';
import MyPage from './component/MyPage';
import BlackList from './component/BlackList';
import OthersPage from './component/OthersPage';
import 'antd/dist/antd.css';

// 程序入口BrowserRouter为路由总组件
// Switch只能有一个他的子组件能被匹配
// Route根据浏览器地址栏的url匹配对应的组件显示到界面上
ReactDOM.render(
  <BrowserRouter>
    <Switch>
      <Route path="/login" exact={true} component={Login}></Route>
      <Route path="/myPage" exact={true} component={MyPage}></Route>
      <Route path="/othersPage/:username/:banned_user_id" exact={true} component={OthersPage}></Route>
      <Route path="/blackList" exact={true} component={BlackList}></Route>
      <Route path="/detail/:mid" exact={true} component={Detail}></Route>
      <Route path="/" exact={true} component={App}></Route>
    </Switch>
  </BrowserRouter>,
  document.getElementById('root')
);
