import { Card, Form, Input,message, Button } from 'antd';
import styles from '../css/login.module.css';
import api from '../api/index.js';

const layout = {
  labelCol: { span: 7 },
  wrapperCol: { span: 25 },
};
const tailLayout = {
  wrapperCol: {  span: 32 },
};

function Login(props) {
  const onFinish = values => {
    api.post('/login/', values)
      .then(({ data }) => {
        console.log(data);
        if (data.success) {
          props.history.push('/');
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        console.log('Success:', values);
      });
  };

  return (
    <div className={styles.bg}>
      <Card title="Login" bordered={false} style={{ width: 400 }}>
        <Form
          {...layout}
          name="basic"
          initialValues={{ name: '',  password: '' }}
          onFinish={onFinish}
        >
          <Form.Item
            label="Username"
            name="name"
            rules={[{ required: true, message: 'Please input your username!' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[{ required: true, message: 'Please input your password!' }]}
          >
            <Input.Password />
          </Form.Item>

          <Form.Item {...tailLayout}>
            <Button type="primary" htmlType="submit" className={styles.wp100}>
              Login
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}

export default Login;
