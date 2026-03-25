import Template from "./template/Template";
// import ProductDetail from "./products/detail/ProductDetail";
import { Routes, Route } from "react-router-dom";
import Landing from "./landing/Landing";
import ProductList from "./products/ProductList";
import SignUp from "./auth/sign-up";
import Login from "./auth/login";

function App() {
  return (
    <Template>
      <Routes>
        <Route path="/" element={<Landing />} exact />

        <Route path="/login" element={<Login />} exact />
        <Route path="/sign-up" element={<SignUp />} exact />

        <Route path="/products/:page/:category?/:platform?/:minPrice?/:maxPrice?/:search?" element={<ProductList />} exact />
        {/* <Route path="/products/:slug" element={<ProductDetail />} /> */}
      </Routes>
    </Template>
  );
}

export default App;