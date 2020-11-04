import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
// import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import Login from './component/Login';
import Detail from './component/Detail';
import 'antd/dist/antd.css';

ReactDOM.render(
  <BrowserRouter>
    <Switch>
      <Route path="/login" exact={true} component={Login}></Route>
      <Route path="/detail/:mid" exact={true} component={Detail}></Route>
      <Route path="/" exact={true} component={App}></Route>
    </Switch>
  </BrowserRouter>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals(console.log);
