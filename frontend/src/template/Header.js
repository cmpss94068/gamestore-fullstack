import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from 'axios';

function Header() {

    const [openedDrawer, setOpenedDrawer] = useState(false)
    const [orderCount, setOrderCount] = useState(null);
    const jwtToken = localStorage.getItem('jwtToken');
    const userName = localStorage.getItem('userName');
    const navigate = useNavigate();

    useEffect(() => {
        if (jwtToken) {
            let getOrderCount = "http://127.0.0.1:8000/api/shoppingcart/order_count/";

            axios.defaults.headers.common['Authorization'] = `Bearer ${jwtToken}`;

            axios.get(getOrderCount)
                .then((response) => {
                    console.log(response.data);
                    setOrderCount(response.data['order_count']);
                })
                .catch((error) => {
                    console.error('Error fetching order count:', error);
                });
        }
    }, [jwtToken]);

    function toggleDrawer() {
        setOpenedDrawer(!openedDrawer);
    }

    function changeNav(event) {
        if (openedDrawer) {
            setOpenedDrawer(false)
        }
    }

    function signOut() {
        localStorage.removeItem('jwtToken');
        localStorage.removeItem('userName');
        setOrderCount(null);
        navigate('/');
    }

    return (
        <header>
            <nav className="navbar fixed-top navbar-expand-lg navbar-light bg-white border-bottom">
                <div className="container-fluid">
                    <Link className="navbar-brand" to="/" onClick={changeNav}>
                        <FontAwesomeIcon
                            icon={["fab", "bootstrap"]}
                            className="ms-1"
                            size="lg"
                        />
                        <span className="ms-2 h5">Shop</span>
                    </Link>

                    <div className={"navbar-collapse offcanvas-collapse " + (openedDrawer ? 'open' : '')}>
                        <ul className="navbar-nav me-auto mb-lg-0">
                            <li className="nav-item">
                                <Link to="/products/1" className="nav-link" replace onClick={changeNav}>
                                    Explore
                                </Link>
                            </li>
                        </ul>
                        {orderCount != null && (
                            <button type="button" className="btn btn-outline-dark me-3 d-none d-lg-inline">
                                <FontAwesomeIcon icon={["fas", "shopping-cart"]} />
                                <span className="ms-3 badge rounded-pill bg-dark">{orderCount}</span>
                            </button>
                        )}
                        <ul className="navbar-nav mb-2 mb-lg-0">
                            <li className="nav-item dropdown">
                                <a
                                    href="!#"
                                    className="nav-link dropdown-toggle"
                                    data-toggle="dropdown"
                                    id="userDropdown"
                                    role="button"
                                    data-bs-toggle="dropdown"
                                    aria-expanded="false"
                                >
                                    <FontAwesomeIcon icon={["fas", "user-alt"]} />
                                </a>
                                <ul
                                    className="dropdown-menu dropdown-menu-end"
                                    aria-labelledby="userDropdown"
                                >
                                    {jwtToken ? (
                                        <>
                                            <li>
                                                <span className="dropdown-item">
                                                    HI! {userName}
                                                </span>
                                            </li>
                                            <li>
                                                <span className="dropdown-item" onClick={signOut}>
                                                    Sign Out
                                                </span>
                                            </li>
                                        </>
                                    ) : (
                                        <>
                                            <li>
                                                <Link to="/login" className="dropdown-item" onClick={changeNav}>
                                                    Login
                                                </Link>
                                            </li>
                                            <li>
                                                <Link to="/sign-up" className="dropdown-item" onClick={changeNav}>
                                                    Sign Up
                                                </Link>
                                            </li>
                                        </>
                                    )}
                                </ul>
                            </li>
                        </ul>
                    </div>

                    <div className="d-inline-block d-lg-none">
                        <button type="button" className="btn btn-outline-dark">
                            <FontAwesomeIcon icon={["fas", "shopping-cart"]} />
                            <span className="ms-3 badge rounded-pill bg-dark">0</span>
                        </button>
                        <button className="navbar-toggler p-0 border-0 ms-3" type="button" onClick={toggleDrawer}>
                            <span className="navbar-toggler-icon"></span>
                        </button>
                    </div>
                </div>
            </nav>
        </header>
    );
}

export default Header;