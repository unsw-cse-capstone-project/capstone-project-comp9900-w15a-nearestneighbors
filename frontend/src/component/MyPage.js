import React, { useEffect, useState } from "react";
import {
  Row,
  Col,
  Card,
  message,
  Button,
  Breadcrumb,
  Empty,
  Avatar,
  Image,
} from "antd";
import styles from "../app.module.css";
import api from "../api";
import Header from "./Cheader";
import { HomeOutlined } from "@ant-design/icons";

/* the user's page, mainly the user's comment history and rating. If it is a logged-in user, it also provides a delete function. 
   Next is the display of watchlist, and the service of jumping to the corresponding movie homepage is also provided.
*/

/**
 * myPage component
 * @param props
 * @returns {*}
 * @constructor
 */
function MyPage(props) {
  const [userInfo, setUserInfo] = useState({});

  const gotoMyBlackList = (props) => {
    props.history.push("/blackList");
  };

  const getMyPageInfo = () => {
    api
      .get("/my_page/", {})
      .then(({ data }) => {
        if (data.success) {
          setUserInfo(data);
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        console.log(e);
      });
  };

  useEffect(() => getMyPageInfo(), []);

  const deleteReview = (movie_id) => {
    api
      .get("/my_page/my_reviews/get_review/delete_review/", {
        params: { movie_id },
      })
      .then(() => {
        getMyPageInfo();
      })
      .catch((e) => {
        console.log(e);
      });
  };

  return (
    <div>
      <Header {...{ props }}></Header>
      <div
        className={styles.bgMypage}
        style={{ minHeight: "calc(100vh - 64px)" }}
      >
        <div
          style={{
            width: "1040px",
            margin: "0 auto",
            opacity: "0.9",
            padding: "16px",
            boxShadow: "-2px 2px 11px #999999",
            background: "white",
            minHeight: "calc(100vh - 64px)",
          }}
        >
          <Breadcrumb>
            <Breadcrumb.Item>
              <a onClick={() => props.history.push("/")}>
                <HomeOutlined style={{ marginRight: "8px" }} />
                Home
              </a>
            </Breadcrumb.Item>
            <Breadcrumb.Item>My Page</Breadcrumb.Item>
          </Breadcrumb>
          <div>
            <h1>
              <Avatar src={userInfo.profile_photo} alt="user avatar" />
              <span>{userInfo.username}</span>

              <Button type="link" onClick={() => gotoMyBlackList(props)}>
                My BlackList
              </Button>
            </h1>
            <h2>Reviews</h2>
            <div style={{ maxHeight: "400px", overflowY: "auto" }}>
              {(userInfo.top_reviews || []).map(
                ({ movie_name, rating_number, review_comment, movie_id }) => {
                  return (
                    <div key={movie_name}>
                      <Row>
                        <Col span={8}>
                          <b>{movie_name}</b>
                        </Col>
                        <Col span={1} offset={15}>
                          <b>{rating_number}</b>
                        </Col>
                      </Row>
                      <p>
                        {review_comment}
                        <Button
                          type="link"
                          onClick={() => deleteReview(movie_id)}
                        >
                          Delete
                        </Button>
                      </p>
                    </div>
                  );
                }
              )}
            </div>

            <Row>
              <Col span={8}>
                <h1>WatchList</h1>
              </Col>
              {/*<Col span={4} offset={12}><b>view & edit watchList</b></Col>*/}
            </Row>

            <Row
              justify="space-around"
              style={{
                marginBottom: "20px",
                width: "1024px",
                overflowX: "auto",
              }}
            >
              {(userInfo.wishlist || []).map(
                ({
                  name,
                  mid,
                  poster = "https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png",
                }) => {
                  return (
                    <Col key={name}>
                      <Card
                        hoverable
                        onClick={() => {
                          props.history.push("/detail/" + mid);
                        }}
                        className={styles.wd}
                        cover={<img alt="example" src={poster} />}
                      >
                        <Card.Meta title={name} description="" />
                      </Card>
                    </Col>
                  );
                }
              )}
              {(userInfo.wishlist || []).length === 0 && <Empty />}
            </Row>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MyPage;
