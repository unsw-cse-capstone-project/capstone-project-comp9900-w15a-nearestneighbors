import { List, Avatar, message, Button, Breadcrumb } from 'antd';
import { useEffect, useState } from "react";
import api from "../api";
import Header from './Cheader';
import React from "react";
import { HomeOutlined } from '@ant-design/icons';
import styles from "../app.module.css";
// 黑名单页面
function BlackList(props) {
  const [list, setList] = useState([]);

  const getBanList = () => {
    api
      .get('/my_page/my_bannedlist/')
      .then(({ data }) => {
        if (data.success) {
          setList(data);
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        console.log(e);
      })
  };

  const removeBlack = (uid) => {
    api
      .get('/my_page/my_bannedlist/remove_from_bannedlist/', { params: { banned_user_id: uid } })
      .then(({ data }) => {
        if (data.success) {
          getBanList();
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        console.log(e);
      })
  };

  useEffect(() => getBanList(), []);

  return (
    <>
      <Header {...{ props }}></Header>
      <div className={styles.bgMypage} style={{ minHeight: 'calc(100vh - 64px)' }}>
        <div style={{
          width: '1040px', margin: '0 auto',
          opacity: '0.9',padding: '16px',boxShadow: '-2px 2px 11px #999999',
          background: 'white', minHeight: 'calc(100vh - 64px)' }}>
          <Breadcrumb>
            <Breadcrumb.Item>
              <a onClick={() => props.history.push('/')}>
                <HomeOutlined style={{marginRight: '8px'}}/>
                Home
              </a>
            </Breadcrumb.Item>
            <Breadcrumb.Item>My BlackList</Breadcrumb.Item>
          </Breadcrumb>
          <div style={{ width: '1024px', margin: '0 auto', marginTop: '20px' }}>
            <h1>My BlackList</h1>
            <List
              itemLayout="horizontal"
              dataSource={list.bannedlist}
              renderItem={item => (
                <List.Item
                  actions={[<Button key="list-loadmore-edit" onClick={() => removeBlack(item.uid)}>Remove</Button>]}
                >
                  <List.Item.Meta
                    avatar={<Avatar src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png" />}
                    title={<a href="https://ant.design">{item.name}</a>}
                  />
                </List.Item>
              )}
            />
          </div>
        </div>
      </div>
    </>
  );
}
export default BlackList;
