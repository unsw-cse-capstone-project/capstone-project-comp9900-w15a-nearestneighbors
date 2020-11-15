import React, { useEffect, useMemo, useState } from 'react';
import {
  Descriptions,
  Row,
  Col,
  Comment,
  Button,
  Avatar,
  Card,
  Form,
  Input,
  message,
  Tooltip,
  Breadcrumb,
  Rate
} from 'antd';
import { UserOutlined } from '@ant-design/icons';
import moment from 'moment';
import styles from "../app.module.css";
import api from '../api';
import Header from './Cheader';
import { HomeOutlined } from '@ant-design/icons';
// 点击电影后进入的详情页面


// 这是评论的组件
const Editor = ({ onChange, onSubmit, submitting, value, ratingChange, valueRating }) => (
  <>
    <Form.Item>
      <Input.TextArea rows={4} onChange={onChange} value={value} />
    </Form.Item>
    <Form.Item>
      <Rate onChange={ratingChange} value={desc.indexOf(Math.floor(valueRating)) + 1} />
      <span className="ant-rate-text">{ valueRating }</span>
    </Form.Item>
    <Form.Item>
      <Button htmlType="submit" loading={submitting} onClick={onSubmit} type="primary">
        Add Comment
      </Button>
    </Form.Item>
  </>
);

const desc = [1, 2, 3, 4, 5];

function Detail(props) {
  const [detail, setDetail] = useState({});
  const [similar, setSimilar] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [value, setValue] = useState('');
  const [valueRating, setV] = useState(0);

  const getDetail = () => {
    api
      .get('/movies/detail/', { params: { movie_id: props.match.params.mid } })
      .then(({ data }) => {
        if (data.success) {
          setDetail(data.movie[0]);
          setSimilar(data.similar_movies);
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        console.log(e);
      })
  };

  useEffect(() => getDetail(), []);

  const comment = () => {
    if (!value) return;
    setSubmitting(true);

    api
      .post('/movies/detail/new_review/', {
        movie_id: props.match.params.mid,
        review_comment: value,
        rating_number: valueRating,
      })
      .then(({ data }) => {
        setSubmitting(false);
        if (data.success) {
          getDetail();
          setValue('');
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        setSubmitting(false);
        console.log(e);
      })
  };

  const addToWishList = () => {
    api
      .get('/movies/detail/add_to_wishlist/', { params: { movie_id: props.match.params.mid } })
      .then(({ data }) => {
        if (data.success) {
          message.success(data.msg);
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        setSubmitting(false);
        console.log(e);
      })
  };

  const gotoBlack = (props, user_name, user_id) => {
    if (user_id === JSON.parse((localStorage.getItem('user') || {})).user_id) {
      return message.error('Can\'t go to othersPage! It it yourself account!');
    }

    props.history.push(`/othersPage/${user_name}/${user_id}`);
  };

  const ratingChange = (v) => {
    setV(v);
  };

  return <>
    <Header {...{ props }}></Header>
    <div style={{ width: '1024px', margin: '0 auto' }}>
      <Breadcrumb style={{ paddingTop: '8px', paddingBottom: '8px' }}>
        <Breadcrumb.Item>
          <a onClick={() => props.history.push('/')}>
            <HomeOutlined style={{marginRight: '8px'}}/>
            Home
          </a>
        </Breadcrumb.Item>
        <Breadcrumb.Item>Detail Page</Breadcrumb.Item>
      </Breadcrumb>
      <Row>
        <Col span={7} flex>
          <img src={detail.poster} alt="" style={{ width: '100%', height: '100%' }}/>
        </Col>
        <Col span={17}>
          <Descriptions title="Film Detail" column={1} bordered>
            <Descriptions.Item label="Film Name">{ detail.name }</Descriptions.Item>
            <Descriptions.Item label="Director">{ detail.director }</Descriptions.Item>
            <Descriptions.Item label="Genre">{ (detail.genre || []).join(' , ') }</Descriptions.Item>
            <Descriptions.Item label="Average Rating">{ detail.average_rating }</Descriptions.Item>
            <Descriptions.Item label="">
              <Button type="primary" onClick={addToWishList}>Add to Wishlist</Button>
            </Descriptions.Item>
          </Descriptions>
        </Col>
      </Row>
      <Row>
        <Col span={24}>
          <h1>Description</h1>
        </Col>
        <Col>
          <p>{ detail.description }</p>
        </Col>
      </Row>
      <Row>
        <Col span={24}>
          <h1>Reviews</h1>
        </Col>
        {
          (detail.reviews || []).map(({ user_name, review_comment, date, user_id, rating_number }) => {
            return (
              <Col key={user_name}>
                <Comment
                  author={<a onClick={() => gotoBlack(props, user_name, user_id)}>{ user_name }</a>}
                  avatar={
                    <Avatar style={{ backgroundColor: '#87d068' }} icon={<UserOutlined />} />
                  }
                  content={
                    <p>{ review_comment }</p>
                  }
                  datetime={
                    <div style={{ display: 'flex' }}>
                      <Tooltip title={moment(new Date(date)).format('YYYY-MM-DD HH:mm:ss')}>
                        <span>{moment(new Date(date)).fromNow()}</span>
                      </Tooltip>
                      <div style={{ marginLeft: '80px' }}>
                        <Rate disabled value={desc.indexOf(Math.floor(rating_number)) + 1} />
                        <span className="ant-rate-text">{Number((rating_number)).toFixed(1)}</span>
                      </div>
                    </div>
                  }
                />
              </Col>
            );
          })
        }
      </Row>
      <Row>
        <Col span={24}>
          <Comment
            avatar={
              <Avatar
                src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
                alt="Han Solo"
              />
            }
            content={
              <div>
                <Editor
                  onChange={(e) => setValue(e.target.value)}
                  onSubmit={comment}
                  submitting={submitting}
                  value={value}
                  valueRating={valueRating}
                  ratingChange={ratingChange}
                />
              </div>
            }
          />
        </Col>
      </Row>
      <Row>
        <Col span={24}>
          <h1>Similar Movies</h1>
        </Col>
      </Row>
      <Row justify="space-between" style={{ marginBottom: '16px', maxHeight: '600px', overflowY: 'auto' }}>
        {
          similar.map(({ poster, name, mid }) => {
            return (
              <Col key={mid}>
                <Card
                  hoverable
                  onClick={() => {
                    props.history.push('/detail/' + mid);
                    document.location.reload();
                  }}
                  className={styles.wd}
                  cover={<img alt="example" src={poster}/>}
                >
                  <Card.Meta title={name} description=""/>
                </Card>
              </Col>
            );
          })
        }

      </Row>
    </div>
  </>
}


export default Detail;
