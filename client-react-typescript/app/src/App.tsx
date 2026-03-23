import styled from 'styled-components';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'

import StorePage from './pages/StorePage.tsx';
import ProductPage from './pages/ProductPage.tsx';
import CartPage from './pages/CartPage.tsx';
import OrdersPage from './pages/OrdersPage.tsx';
import OrderCheckPaymentPage from './pages/OrderCheckPaymentPage.tsx';
import { fetchUser } from './slices/UserSlice.ts';
import { fetchCart } from './slices/CartSlice.ts';
import { fetchOrders } from './slices/OrdersSlice.ts';
import { useAppDispatch, useAppSelector } from './store.ts';

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
    const dispatch = useAppDispatch()

    const {user, loading: userLoading} = useAppSelector(state => state.user)
    const {cart, loading: cartLoading} = useAppSelector(state => state.cart)
    const {orders, loading: ordersLoading} = useAppSelector(state => state.orders)

    useEffect(() => {
        dispatch(fetchUser())
        dispatch(fetchCart())
        dispatch(fetchOrders())
    }, [])

    useEffect(() => console.log(user), [user])
    useEffect(() => console.log(cart), [cart])
    useEffect(() => console.log(orders), [orders])


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

