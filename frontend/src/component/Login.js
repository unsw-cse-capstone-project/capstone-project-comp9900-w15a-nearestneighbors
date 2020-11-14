import { Card, Form, Input,message, Button, Modal } from 'antd';
import styles from '../css/login.module.css';
import api from '../api/index.js';
import { useState } from 'react';
// 登录组件，处理登录，注册的
const layout = {
  labelCol: { span: 7 },
  wrapperCol: { span: 25 },
};
const tailLayout = {
  wrapperCol: {  span: 32 },
};
const formItemLayout = {
  labelCol: {
    xs: { span: 24 },
    sm: { span: 8 },
  },
  wrapperCol: {
    xs: { span: 24 },
    sm: { span: 16 },
  },
};

function Login(props) {
  const onFinish = values => {
    api.post('/login/', values)
      .then(({ data }) => {
        if (data.success) {
          props.history.push('/');
          localStorage.clear();
          localStorage.setItem('user', JSON.stringify(data));
        } else {
          message.error(data.msg);
        }
      })
      .catch((e) => {
        console.log('Success:', values);
      });
  };

  const [visible, setVisible] = useState(false);
  const [form] = Form.useForm();
  const onFinishRegister = (values) => {
    api.post('/register/', values)
      .then(({ data }) => {
        if (data.success) {
          setVisible(false);
          message.success('register success');
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
            <div style={{ textAlign: 'center' }}>
              Don't have an account?
              <Button type="link" htmlType="button" onClick={() => setVisible(true)}>
                Register
              </Button>
            </div>
          </Form.Item>
        </Form>
      </Card>

      <Modal
        title="Register"
        visible={visible}
        onOk={() => form.submit()}
        onCancel={() => {
          form.resetFields();
          setVisible(false);
        }}
      >
        <Form
          {...formItemLayout}
          form={form}
          name="register"
          onFinish={onFinishRegister}
          scrollToFirstError
        >
          <Form.Item
            name="firstname"
            label={
              <span>firstname&nbsp;</span>
            }
            rules={[{ required: true, message: 'Please input your firstname!', whitespace: true }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="lastname"
            label={
              <span>lastname&nbsp;</span>
            }
            rules={[{ required: true, message: 'Please input your lastname!', whitespace: true }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="name"
            label={
              <span>username&nbsp;</span>
            }
            rules={[{ required: true, message: 'Please input your username!', whitespace: true }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="email"
            label="E-mail"
            rules={[
              {
                type: 'email',
                message: 'The input is not valid E-mail!',
              },
              {
                required: true,
                message: 'Please input your E-mail!',
              },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="password"
            label="Password"
            rules={[
              {
                required: true,
                message: 'Please input your password!',
              },
            ]}
            hasFeedback
          >
            <Input.Password />
          </Form.Item>

          <Form.Item
            name="re_password"
            label="Confirm Password"
            dependencies={['password']}
            hasFeedback
            rules={[
              {
                required: true,
                message: 'Please confirm your password!',
              },
              ({ getFieldValue }) => ({
                validator(rule, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject('The two passwords that you entered do not match!');
                },
              }),
            ]}
          >
            <Input.Password />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

export default Login;
