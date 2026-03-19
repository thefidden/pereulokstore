import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { createPortal } from "react-dom";
import { useLocation } from "react-router-dom";

import { useUser } from "../ContextProviders.jsx";
import ProductCardCompact from "../components/product-card-compact.jsx";
import Loader from "../components/loader.jsx";
import OrderPaymentStatusBox from "../components/order-payment-status-box.jsx";


const Root = styled.div`
    display: flex;
    flex-direction: column;

    gap: 20px;

    .title {
        display: flex;
        justify-content: center;
        align-items: center;

        width: 610px;

        background-color: white;
        border-radius: 100px;

        font-family: 'Jost', serif;
        font-size: 48px;
        font-weight: var(--font-weight-bold);
        color: var(--color-magenta);

        user-select: none;

        will-change: transform, opacity, filter;
        animation: fadeIn 0.3s ease-out forwards;
    }

    .orders {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .order {
        display: grid;
        grid-template-areas: 
            "id _"
            "products-grid products-grid"
            "status price";
        grid-template-columns: 1fr 1fr;

        gap: 20px;

        width: 100%;
        min-height: 100px;
        box-sizing: border-box;
    }

    .orderId {
        grid-area: id;
        border-radius: 100px;
    }

    .orderPrice {
        grid-area: price;
        border-radius: 100px;
    }

    .orderStatus {
        grid-area: status;
        border-radius: 100px;
    }

    .orderId, .orderPrice, .orderStatus {
        display: flex;
        justify-content: center;
        align-items: center;

        padding: 20px 40px;

        background-color: var(--color-magenta);

        font-family: 'Jost', serif;
        font-size: 32px;
        font-weight: var(--font-weight-bold);
        color: white;
        text-wrap: nowrap;

        user-select: none;
        opacity: 0;

        will-change: transform, opacity, filter;
        animation: fadeIn 0.3s ease-out forwards;
    }

    .orderProductsGrid {
        grid-area: products-grid;

        display: flex;
        flex-wrap: wrap;
        justify-content: center;

        gap: 50px;

        box-sizing: border-box;
    }

    .noOrders {
        display: flex;

        justify-content: center;
        align-items: center;

        font-family: 'Jost', serif;
        font-size: 48px;
        font-weight: var(--font-weight-bold);
        color: var(--color-magenta);
        text-transform: uppercase;

        width: 100%;
        min-height: 500px;
        border-radius: 100px;
        user-select: none;

        background-color: white;
        opacity: 0;

        will-change: transform, opacity, filter;
        animation: fadeIn 0.3s ease-out forwards;
    }

    @keyframes fadeIn {
        from {
            filter: blur(30px);
            opacity: 0;
            transform: scale(1.2);
        }
        to {
            filter: blur(0);
            opacity: 1;
            transform: scale(1);
        }
    }
`
const orderStatusTranslation = {
    'pending_payment': 'Ожидает оплаты',
    'paid': 'Оплачен',
    'pending_assembly': 'Собирается',
    'assembled': 'Собран',
    'pending_pickup': 'Готов к выдаче',
    'picked_up': 'Выдан покупателю',
    'finished': 'Завершен',
    'cancelled': 'Отменен'
}

const OrdersPage = () => {
    const location = useLocation()
    const {user, loading: userLoading} = useUser()
    const [stateBoxVisible, setStateBoxVisible] = useState(location.state)

    useEffect(() => console.log(location.state), [location])

    if (userLoading)
        return createPortal(<Loader/>, document.body)

    return (
        <Root>
            {
                stateBoxVisible &&
                createPortal(
                    <OrderPaymentStatusBox
                        orderId = {location.state.orderId}
                        paymentStatus = {location.state.paymentStatus}
                        setBoxVisible = {setStateBoxVisible}
                    />,
                    document.body
                )
            }

            <div className = 'title'>Список заказов</div>

            {user?.orders.length

             ? <div className = 'orders'>
                 {user.orders.reverse().map(order =>
                     <div className = 'order'>
                         <div className = 'orderId'>Заказ: {order.id.toUpperCase()}</div>

                         <div className = 'orderProductsGrid'>{order.products.map((orderItem, index) =>
                             <ProductCardCompact
                                 product = {orderItem.product}
                                 playAnimation = {true}
                                 animationType = 'slideIn'
                                 animationDelay = {0.3 + 0.1 * index}
                             />
                         )}</div>

                         <div className = 'orderPrice'>Сумма: {order.price}₽</div>
                         <div className = 'orderStatus'>Статус: {orderStatusTranslation[order.status]}</div>
                     </div>
                 )}
             </div>

             : <div className = 'noOrders'>ЗАКАЗЫ НЕ ОБНАРУЖЕНЫ</div>
            }
        </Root>
    )
}

export default OrdersPage