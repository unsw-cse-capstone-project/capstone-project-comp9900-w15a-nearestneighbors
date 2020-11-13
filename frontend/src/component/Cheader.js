import { Button, Layout, message, Row, Space, Avatar } from "antd";
import { UserOutlined } from '@ant-design/icons';
import api from "../api";
// 由于很多页面都有共有的Header，单独抽离出了一个公共组件，复用头部导航条
const { Header } = Layout;

function logout(props) {
  api.get('/logout/')
    .then(({ data }) => {
      if (data.success) {
        localStorage.clear();
        props.history.push('/login');
      } else {
        message.error(data.msg);
      }
    })
    .catch((e) => {
      console.log(e);
    })
}

function Cheader({ props }) {

  return <Header style={{backgroundImage: 'linear-gradient(50deg, #816EFE,#227DE8)' }}>
    <Row justify="end">
      <Space>
        <Button type="link" onClick={() => props.history.push('/login')} style={{ color: 'white'}}>Login</Button>
        <Button type="link" onClick={() => logout(props)} style={{ color: 'white'}}>Logout</Button>
        <a onClick={ () => props.history.push('/myPage')}><Avatar  style={{ backgroundColor: '#87d068' }} icon={<UserOutlined />} /></a>
        <span style={{ color: 'white' }}>{(JSON.parse(localStorage.getItem('user')) || {}).username}</span>
      </Space>
    </Row>
  </Header>
}

export default Cheader
