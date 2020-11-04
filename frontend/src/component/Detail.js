import React, { useEffect, useState } from 'react';
import { Descriptions, Row, Col, Comment, Button, Avatar, Card, Form, Input, message, Tooltip } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import moment from 'moment';
import styles from "../app.module.css";
import api from '../api';

const Editor = ({ onChange, onSubmit, submitting, value }) => (
  <>
    <Form.Item>
      <Input.TextArea rows={4} onChange={onChange} value={value} />
    </Form.Item>
    <Form.Item>
      <Button htmlType="submit" loading={submitting} onClick={onSubmit} type="primary">
        Add Comment
      </Button>
    </Form.Item>
  </>
);

function Detail(props) {
  const [detail, setDetail] = useState({});

  useEffect(() => {
    api
      .get('/movies/detail/', { params: { movie_id: props.match.params.mid } })
      .then(({ data }) => {
        if (data.success) {
          setDetail(data.movie[0]);
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        console.log(e);
      })
  }, []);

  return <>
    <div style={{ width: '1024px', margin: '0 auto', marginTop: '20px' }}>
      <Row>
        <Col span={7} flex>
          <img src={detail.poster} alt="" style={{ width: '100%', height: '100%' }}/>
        </Col>
        <Col span={17}>
          <Descriptions title="Film Detail" column={1} bordered>
            <Descriptions.Item label="Film Name">{ detail.name }</Descriptions.Item>
            <Descriptions.Item label="Director">{ detail.director }</Descriptions.Item>
            <Descriptions.Item label="Genre">{ (detail.genre || []).join(' , ') }</Descriptions.Item>
            <Descriptions.Item label="Cast">{ (detail.cast || []).join(' , ') }</Descriptions.Item>
            <Descriptions.Item label="Average Rating">{ detail.average_rating }</Descriptions.Item>
            <Descriptions.Item label="">
              <Button type="primary">Add to Wishlist</Button>
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
          (detail.reviews || []).map(({ user_name, review_comment, date }) => {
            return (
              <Col>
                <Comment
                  author={<a>{ user_name }</a>}
                  avatar={
                    <Avatar style={{ backgroundColor: '#87d068' }} icon={<UserOutlined />} />
                  }
                  content={
                    <p>{ review_comment }</p>
                  }
                  datetime={
                    <Tooltip title={moment(new Date(date)).format('YYYY-MM-DD HH:mm:ss')}>
                      <span>{moment(new Date(date)).fromNow()}</span>
                    </Tooltip>
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
              <Editor
                onChange={() => {}}
                onSubmit={() => {}}
                submitting={() => {}}
                value={{}}
              />
            }
          />
        </Col>
      </Row>

      <Row>
        <Col span={24}>
          <h1>Similar Movies</h1>
        </Col>
      </Row>
      <Row justify="space-between" style={{ marginBottom: '16px' }}>
        <Col>
          <Card
            hoverable
            className={styles.wd}
            cover={<img alt="example" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png"/>}
          >
            <Card.Meta title="Europe Street beat" description="www.instagram.com"/>
          </Card>
        </Col>
        <Col>
          <Card
            hoverable
            className={styles.wd}
            cover={<img alt="example" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png"/>}
          >
            <Card.Meta title="Europe Street beat" description="www.instagram.com"/>
          </Card>
        </Col>
        <Col>
          <Card
            hoverable
            className={styles.wd}
            cover={<img alt="example" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png"/>}
          >
            <Card.Meta title="Europe Street beat" description="www.instagram.com"/>
          </Card>
        </Col>
      </Row>
    </div>
  </>
}


export default Detail;
