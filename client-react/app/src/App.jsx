import { BrowserRouter as Router, Routes, Route, useParams, useSearchParams, Navigate } from 'react-router-dom'
import styled from "styled-components";

import Header from "./components/header.jsx";
import TestPage from "./pages/test.jsx";
import StorePage from "./pages/store-page.jsx";
import ProductPage from "./pages/product-page.jsx";
import AboutPage from "./pages/about.jsx";
import CartPage from "./pages/cart-page.jsx";
import OrdersPage from "./pages/orders-page.jsx";
import OrderCheckPaymentPage from "./pages/order-check-payment.jsx";
import { UserProvider, ProductsProvider, ProductProvider, OrderPaymentStatusProvider } from "./ContextProviders.jsx";

const ProductPageWrapper = () => {
    const {productUUID} = useParams()
    return (
        <ProductProvider productUUID = {productUUID}>
            <ProductPage/>
        </ProductProvider>
    )
}

const StorePageWrapper = () => {
    const [searchParams] = useSearchParams()

    const name = searchParams.get('name')
    const type = searchParams.get('type')
    const priceMin = searchParams.get('price-min')
    const priceMax = searchParams.get('price-max')

    return (
        <ProductsProvider name = {name} type = {type} priceMin = {priceMin} priceMax = {priceMax}>
            <StorePage/>
        </ProductsProvider>
    )
}

const OrderCheckPaymentPageWrapper = () => {
    const params = useParams()
    const [searchParams] = useSearchParams()

    const orderId = params.orderUUID
    const bankOrderId = searchParams.get('orderId')

    return (
        <OrderPaymentStatusProvider orderId = {orderId} bankOrderId = {bankOrderId}>
            <OrderCheckPaymentPage/>
        </OrderPaymentStatusProvider>
    )
}


export default function App() {
    const Root = styled.div`
        max-width: 1440px;

        padding: 40px 0;
        margin: 0 auto;

        display: flex;
        flex-direction: column;
        gap: 80px;

        font-family: 'Jost', serif;
    `

    return (
        <Router>
            <UserProvider>
                <Root>
                    <Header/>
                    <Routes>
                        <Route path = '/' element = {<Navigate to = "/store/?type=suit" replace/>}/>
                        <Route path = '/about' element = {<AboutPage/>}/>
                        <Route path = '/store' element = {<StorePageWrapper/>}/>
                        <Route path = '/products/:productUUID' element = {<ProductPageWrapper/>}/>
                        <Route path = '/cart' element = {<CartPage/>}/>
                        <Route path = '/orders' element = {<OrdersPage/>}/>
                        <Route path = '/orders/:orderUUID/payment/check' element = {<OrderCheckPaymentPageWrapper/>}/>

                        <Route path = '/test' element = {<TestPage/>}/>
                    </Routes>
                </Root>
            </UserProvider>
        </Router>
    )
}