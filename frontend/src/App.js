import { Layout, Input, Space, Card, Row, Col, Rate, message, Spin, Tabs, Select } from "antd";
import { useState, useMemo } from 'react';
import styles from './app.module.css';
import { useEffect } from "react";
import api from './api';
import './css/common.css';
import Cheader from './component/Cheader';

const { Footer, Content } = Layout;
const { Meta } = Card;

const directors = [
  'Peter Jackson',
  'Michael Bay',
  'Steven Spielberg',
  'Christopher Nolan',
  'Gore Verbinski',
  'Sam Raimi',
  'Bryan Singer',
  'Quentin Tarantino',
  'David Yates',
  'Zack Snyder',
];

const genres = [
  'Action',
  'Adventure',
  'Animation',
  'Comedy',
  'Crime',
  'Drama',
  'Family',
  'Fantacy',
  'Fantasy',
  'History',
  'Horror',
  'Mystery',
  'Romance',
  'Science fiction',
  'Thriller',
  'War',
  'Western',
];

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
    return <Row key={i} style={{ marginBottom: '16px' }} className="main-list" gutter={[20,20]}>
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
                    <Rate disabled value={desc.indexOf(Math.floor(average_rating || rating)) + 1} />
                    <span className="ant-rate-text">{Number((average_rating || rating)).toFixed(1)}</span>
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
  const desc = useMemo(() => [1, 2, 3, 4, 5], []);
  const [moves, setMovies] = useState([]);
  const [searchValue, setSearchValue] = useState(false);
  const [spinning, setSpinning] = useState(true);
  const [currentTab, setCurrentTab] = useState('1');
  const [genre, setGen] = useState('Action');
  const [director, setDir] = useState('Peter Jackson');

  const getMovies = () => {
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
  };
  useEffect(() => getMovies(), [searchValue]);
  const tabChange = (key) => {
    setCurrentTab(key);
    if (key === '1') getMovies();
    if (key === '2') mostPopular();
    if (key === '3') viewByGenre();
    if (key === '4') viewByDirector();
  };
  const mostPopular = () => {
    setSpinning(true);
    api.get('/index/')
      .then(({ data }) => {
        setSpinning(false);
        setMovies(data.most_popular);
      })
      .catch((e) => {
        setSpinning(false);
        console.log(e)
      });
  };
  const viewByGenre = (data) => {
    setSpinning(true);
    api.get('/browse_by_genre/', { params: { genre: data ? data : genre } })
      .then(({ data }) => {
        setSpinning(false);
        setMovies(data.movies);
      })
      .catch((e) => {
        setSpinning(false);
        console.log(e)
      });
  };
  const viewByDirector = (data) => {
    setSpinning(true);
    api.get('/browse_by_director/', { params: { director: data ? data : director } })
      .then(({ data }) => {
        setSpinning(false);
        setMovies(data.movies);
      })
      .catch((e) => {
        setSpinning(false);
        console.log(e)
      });
  };
  const genreChange = (genre) => {
    setGen(genre);
    viewByGenre(genre);
  };
  const directorChange = (director) => {
    setDir(director);
    viewByDirector(director);
  };

  function getCurrentTabMovie() {
    return <Spin tip="Loading..." spinning={spinning}>
      <Row className={styles.mb16} justify="center">
        <Space>
          {
            currentTab === '1' && <Input.Search
              placeholder="input movie name, description, or genre..."
              allowClear
              enterButton="Search"
              size="large"
              onSearch={onSearch}
              style={{width: '600px'}}
            />
          }

          {
            currentTab === '3' && <Select onChange={genreChange} defaultValue="Action" size='large' style={{width: '200px'}}>
              {
                genres.map(n => <Select.Option value={n} key={n}>{n}</Select.Option>)
              }
            </Select>
          }

          {
            currentTab === '4' && <Select onChange={directorChange} defaultValue="Peter Jackson" size='large' style={{width: '200px'}}>
              {
                directors.map(n => <Select.Option value={n} key={n}>{n}</Select.Option>)
              }
            </Select>
          }
        </Space>
      </Row>
      { genRows(getSlicedArr(moves), props, desc) }
    </Spin>
  }

  return (
    <>
      <Layout style={{ minWidth: '1590px', }}>
        <Cheader {...{ props }}></Cheader>
        <Content className={`${styles.contentHeight} ${styles.pd} main-list`} style={{minHeight: 'calc(100vh - 134px)'}}>
          <Tabs defaultActiveKey="1" onChange={tabChange}>
            <Tabs.TabPane tab="All" key="1"></Tabs.TabPane>
            <Tabs.TabPane tab="Most Popular" key="2"></Tabs.TabPane>
            <Tabs.TabPane tab="View By Genre" key="3"></Tabs.TabPane>
            <Tabs.TabPane tab="View By Director" key="4"></Tabs.TabPane>
          </Tabs>
          {  getCurrentTabMovie() }
        </Content>
        <Footer style={{ textAlign: 'center' }}>FilmFinder ©2020 Created by Zzmilk</Footer>
      </Layout>
    </>
  );
}



export default App;
