import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });

    const AccountChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const Register = async (e) => {
        e.preventDefault();
        if (!formData.username) {
            alert("使用者帳號未填寫");
            return;
        } else if (!formData.password) {
            alert("使用者密碼未填寫");
            return;
        }

        var formdata = new FormData();
        formdata.append("username", formData.username);
        formdata.append("password", formData.password);

        var requestOptions = {
            method: 'POST',
            body: formdata,
            redirect: 'follow',
        };

        fetch("http://127.0.0.1:8000/api/auth/token/", requestOptions)
            .then(response => {
                if (response.ok) {
                    response.json().then(data => {
                        localStorage.setItem('jwtToken', data.access);
                        localStorage.setItem('userName', formData.username);
                    });
                    navigate('/');
                } else {
                    // 解析后端返回的错误消息
                    response.json().then(data => {
                        alert('帳號密碼有誤');
                    });
                }
            })
            .catch((err) => {
                console.log(err.message);
            });
    };

    return (
        <div className="container mt-5 py-4 px-xl-5">
            <div className="row my-4">
                <div className="col-md-6 offset-md-3 col-lg-4 offset-lg-4">
                    <div className="card border-0 shadow-sm">
                        <div className="card-body px-4">
                            <h4 className="card-title fw-bold mt-2 mb-4">Sign in</h4>
                            <form className="row g-2" onSubmit={Register}>
                                <div className="col-md-12">
                                    <label className="form-label">Account</label>
                                    <input
                                        type="text"
                                        name="username"
                                        className="form-control"
                                        value={formData.username}
                                        onChange={AccountChange}
                                    />
                                </div>
                                <div className="col-md-12">
                                    <label className="form-label">Password</label>
                                    <input
                                        type="password"
                                        name="password"
                                        className="form-control"
                                        value={formData.password}
                                        onChange={AccountChange}
                                    />
                                </div>
                                <div className="col-md-12 mt-4">
                                    <button type="submit" className="btn btn-primary w-100">
                                        login
                                    </button>
                                </div>
                            </form>
                        </div>
                        <hr className="text-muted my-0" />
                        <div className="text-center p-3">
                            Don&lsquo;t hanve an account?{" "}
                            <a href="/sign-up" className="text-decoration-none fw-medium" style={{ color: "blue", fontWeight: 500, textDecoration: "none" }} a>
                                Login
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
        </div>
    );
}

export default Login;