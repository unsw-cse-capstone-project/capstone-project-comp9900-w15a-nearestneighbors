import { Layout, Input, Space, Card, Row, Col, Rate, Button, message } from "antd";
import { useState, useMemo } from 'react';
import styles from './app.module.css';
import { useEffect } from "react";
import api from './api';
import './css/common.css';

const { Header, Footer, Content } = Layout;
const { Meta } = Card;

function getSlicedArr(arr, len = 5) {
  let movies = [];

  while (arr.length >= len) {
    movies.push(arr.slice(0, len));
    arr = arr.slice(len);
  }

  if (arr.length !== 0) {
    movies.push(arr);
  }

  return movies
}

function logout(props) {
  api.get('/logout/')
    .then(({ data }) => {
      if (data.success) {
        props.history.push('/login');
      } else {
        message.error(data.msg);
      }
    })
    .catch((e) => {
      console.log(e);
    })
}

function genRows(allRowData, props, desc) {

  return allRowData.map((singleRow, i) => {
    return <Row key={i} justify="space-between" style={{ marginBottom: '16px' }} className="main-list">
      {
        singleRow.map(({ name, poster, mid, average_rating, rating }) => {
          return (
            <Col key={mid} onClick={() => props.history.push('/detail/' + mid)}>
              <Card
                hoverable
                className={styles.wd}
                cover={<img alt="example" src={poster} style={{ height: '400px' }}/>}
              >
                <div style={{marginBottom: '8px' }}>
                  <span>
                    <Rate disabled value={desc.indexOf(average_rating || rating) + 1} />
                    <span className="ant-rate-text">{average_rating || rating}</span>
                  </span>
                </div>
                <Meta title={name}/>
              </Card>
            </Col>
          );
        })
      }
    </Row>
  });
}

function App(props) {
  const onSearch = value => {
    if (value === '') return setSearchValue(!searchValue);

    api.get('/search/', { params: { search: value } })
      .then(({ data }) => {
        if (data.success) {
          setMovies(data.result);
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        console.log(e);
      })
  };
  const desc = useMemo(() => [4.6, 4.7, 4.8, 4.9, 5], []);
  const [moves, setMovies] = useState([]);
  const [searchValue, setSearchValue] = useState(false);

  useEffect(() => {
    api.get('/movies/')
      .then(({ data }) => {
        if (data.success) {
          setMovies(data.movies);
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => console.log(e))
  }, [searchValue]);

  return (
    <>
      <Layout style={{ minWidth: '1590px', }}>
        <Header>
          <Row justify="end">
            <Space>
              <Button type="link" onClick={() => props.history.push('/login')}>Login</Button>
              <Button type="link" onClick={() => logout(props)}>Logout</Button>
            </Space>
          </Row>
        </Header>
        <Content className={`${styles.contentHeight} ${styles.pd} main-list`}>
          <Row className={styles.mb16} justify="center">
            <Space>
              <Input.Search
                placeholder="input movie name, description, or genre..."
                allowClear
                enterButton="Search"
                size="large"
                onSearch={onSearch}
                style={{width: '600px'}}
              />
            </Space>
          </Row>
          { genRows(getSlicedArr(moves), props, desc) }
        </Content>
        <Footer style={{ textAlign: 'center' }}>FilmFinder ©2020 Created by Zzmilk</Footer>
      </Layout>
    </>
  );
}

export default App;
