import styled from "styled-components";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

import { useAppSelector } from "../store.ts";
import type { Order } from "../interfaces/OrderInterface.ts";
import type { OrderItem } from "../interfaces/OrderItemInterface.ts";
import Loader from "../components/Loader.tsx";
import OrderItemCard from "../components/OrderItemCard.tsx";
import OrderPaymentStatusBox from "../components/OrderPaymentStatusBox.tsx";

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

export default function OrdersPage() {
    const location = useLocation()

    const { orders, loading: ordersLoading } = useAppSelector(state => state.orders)
    const [orderPaymentStatusBoxVisible, setOrderPaymentStatusBoxVisible] = useState(!!location.state?.paymentStatus)

    useEffect(() => console.log(location.state), [])

    if (ordersLoading)
        return <Loader />

    return (
        <Root>
            {
                orderPaymentStatusBoxVisible &&
                <OrderPaymentStatusBox
                    orderId={ location.state.orderId }
                    paymentStatus={ location.state.paymentStatus }
                    setOrderPaymentStatusBoxVisible={ setOrderPaymentStatusBoxVisible }
                />
            }

            <div className="title">Список заказов</div>

            {
                !!orders

                    ? <div className="orders">{
                        [...orders].reverse().map((order: Order) =>
                            <div className="order">
                                <div className="orderId">Заказ: { order.id.toUpperCase() }</div>

                                <div className="orderProductsGrid">{
                                    order.items.map((orderItem: OrderItem, index: number) =>
                                        <OrderItemCard orderItem={ orderItem } animationDelay={ 0.3 + 0.1 * index } />
                                    )
                                }</div>

                                <div className="orderPrice">Сумма: { order.price }₽</div>
                                <div className="orderStatus">Статус: { orderStatusTranslation[order.status] }</div>
                            </div>
                        )
                    }</div>

                    : <div className="noOrders">ЗАКАЗЫ НЕ ОБНАРУЖЕНЫ</div>
            }
        </Root>
    )
}