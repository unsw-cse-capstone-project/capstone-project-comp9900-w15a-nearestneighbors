import { Layout, Input, Space, Card, Row, Col, Rate, Button, message, Spin } from "antd";
import { useState, useMemo } from 'react';
import styles from './app.module.css';
import { useEffect } from "react";
import api from './api';
import './css/common.css';
import Cheader from './component/Cheader';

const { Header, Footer, Content } = Layout;
const { Meta } = Card;

/**
 * 切割电影数组为二维数组，方便生成ui的时候遍历
 * @param arr
 * @param len
 * @returns {Array}
 */
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

    setSpinning(true);
    api.get('/search/', { params: { search: value } })
      .then(({ data }) => {
        setSpinning(false);
        if (data.success) {
          setMovies(data.result);
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        setSpinning(false);
        console.log(e);
      })
  };
  const desc = useMemo(() => [4.6, 4.7, 4.8, 4.9, 5], []);
  const [moves, setMovies] = useState([]);
  const [searchValue, setSearchValue] = useState(false);
  const [spinning, setSpinning] = useState(true);

  useEffect(() => {
    setSpinning(true);
    api.get('/movies/')
      .then(({ data }) => {
        setSpinning(false);
        if (data.success) {
          setMovies(data.movies);
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        setSpinning(false);
        console.log(e)
      });
  }, [searchValue]);

  return (
    <>
      <Layout style={{ minWidth: '1590px', }}>
        <Cheader {...{ props }}></Cheader>
        <Content className={`${styles.contentHeight} ${styles.pd} main-list`} style={{minHeight: 'calc(100vh - 134px)'}}>
          <Spin tip="Loading..." spinning={spinning}>
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
          </Spin>
        </Content>
        <Footer style={{ textAlign: 'center' }}>FilmFinder ©2020 Created by Zzmilk</Footer>
      </Layout>
    </>
  );
}

export default App;
