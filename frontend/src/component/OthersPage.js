import React, { useEffect, useState } from 'react';
import { Row, Col, Card, message, Button, Breadcrumb, Empty } from 'antd';
import styles from "../app.module.css";
import api from "../api";
import Header from './Cheader';
import { HomeOutlined } from '@ant-design/icons';
// 其他用户的个人详情页面
function OthersPage(props) {

  const [userInfo, setUserInfo] = useState({});

  useEffect(() => {
    api
      .get('/user_page/', { params: { username: props.match.params.username }})
      .then(({ data }) => {
        if (data.success) {
          setUserInfo(data)
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        console.log(e);
      })
  }, []);

  const addToBlackList = () => {
    api
      .get('/user_page/add_to_bannedlist/', { params: { banned_user_id: props.match.params.banned_user_id } })
      .then(({ data }) => {
        if (data.success) {
          message.success(data.msg);
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        console.log(e);
      })
  };

  return <>
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
          <Breadcrumb.Item>Others Page</Breadcrumb.Item>
        </Breadcrumb>
        <div style={{ width: '1024px', margin: '0 auto', marginTop: '20px' }}>
          <h1>
            <span>{ userInfo.username }</span>
            <Button type="link" onClick={() => addToBlackList()}>Add To BlackList</Button>
          </h1>
          <h2>Reviews</h2>
          <div style={{maxHeight: '400px', overflowY: 'auto'}}>
            {
              (userInfo.top_reviews || []).map(({ movie_name, rating_number, review_comment }) => {
                return <div key={movie_name}>
                  <Row>
                    <Col span={8}><b>{ movie_name }</b></Col>
                    <Col span={1} offset={15}><b>{ rating_number }</b></Col>
                  </Row>
                  <p>{ review_comment }</p>
                </div>
              })
            }
          </div>


          <Row>
            <Col span={8}><h1>WatchList</h1></Col>
            {/*<Col span={4} offset={12}><b>view & edit watchList</b></Col>*/}
          </Row>

          <Row justify="space-around" style={{marginBottom: '20px', width: '1024px', overflowX: 'auto'}}>
            {
              (userInfo.wishlist || []).map(({ name, poster = 'https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png' }) => {
                return <Col key={name}>
                  <Card
                    hoverable
                    className={styles.wd}
                    cover={<img alt="example" src={poster}/>}
                  >
                    <Card.Meta title={name} description=""/>
                  </Card>
                </Col>;
              })
            }
            {
              (userInfo.wishlist || []).length === 0 && <Empty />
            }
          </Row>
        </div>
      </div>
    </div>
  </>
}

export default OthersPage;
