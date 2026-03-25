import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SignUp() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        password2: ''
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
        } else if (!formData.password2) {
            alert("確認密碼未填寫");
            return;
        } else if (formData.password !== formData.password2) {
            alert("密碼與確認密碼不同");
            return;
        }

        var formdata = new FormData();
        formdata.append("username", formData.username);
        formdata.append("password", formData.password);
        formdata.append("password2", formData.password2);

        var requestOptions = {
            method: 'POST',
            body: formdata,
            redirect: 'follow',
        };

        fetch("http://127.0.0.1:8000/api/auth/register/", requestOptions)
            .then(response => {
                if (response.ok) {
                    alert('註冊成功')
                    navigate('/login');
                } else {
                    // 解析后端返回的错误消息
                    response.json().then(data => {
                        alert(data.password);
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
                            <h4 className="card-title fw-bold mt-2 mb-4">Sign Up</h4>
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
                                <div className="col-md-12">
                                    <label className="form-label">Confirm Password</label>
                                    <input
                                        type="password"
                                        name="password2"
                                        className="form-control"
                                        value={formData.password2}
                                        onChange={AccountChange}
                                    />
                                </div>
                                <div className="col-md-12 mt-4">
                                    <button type="submit" className="btn btn-primary w-100">
                                        Register
                                    </button>
                                </div>
                            </form>
                        </div>
                        <hr className="text-muted my-0" />
                        <div className="text-center p-3">
                            Already have an account?{" "}
                            <a href="/login" className="text-decoration-none fw-medium" style={{ color: "blue", fontWeight: 500, textDecoration: "none" }} a>
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
        </div>
    );
}

export default SignUp;