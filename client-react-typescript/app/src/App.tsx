import styled from "styled-components";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import StorePage from "./pages/StorePage.tsx";
import ProductPage from "./pages/ProductPage.tsx";
import CartPage from "./pages/CartPage.tsx";
import OrdersPage from "./pages/OrdersPage.tsx";
import OrderCheckPaymentPage from "./pages/OrderCheckPaymentPage.tsx";

const Root = styled.div`
    max-width: 1440px;

    padding: 40px 0;
    margin: 0 auto;

    display: flex;
    flex-direction: column;
    gap: 80px;

    font-family: 'Jost', serif;
`

export default function App() {
    return (
        <Router>
            <Root>
                <Routes>
                    <Route path="/" element={<Navigate to="store?type=suit" replace/>}/>
                    <Route path="/store" element={<StorePage/>}/>
                    <Route path="/product/:productUUID" element={<ProductPage/>}/>
                    <Route path="/cart" element={<CartPage/>}/>
                    <Route path="/orders" element={<OrdersPage/>}/>
                    <Route path="/orders/:orderUUID/payment/check" element={<OrderCheckPaymentPage/>}/>
                </Routes>
            </Root>
        </Router>
    )
}

