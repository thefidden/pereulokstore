import styled from "styled-components";
import { useAppDispatch, useAppSelector } from "../store.ts";
import Loader from "../components/Loader.tsx";
import type { CartItem } from "../interfaces/CartItemInterface.ts";
import CartItemCard from "../components/CartItemCard.tsx";
import { createOrder } from "../slices/OrdersSlice.ts";
import { useLocation } from "react-router-dom";
import { useState } from "react";
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

        will-change: opacity, filter, transform;
        animation: fadeIn 0.3s ease-out forwards;
    }

    .cart {
        display: grid;
        grid-template-areas: 
            "products-grid products-grid"
            "price buy-button";
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }

    .totalPrice {
        grid-area: price;
        justify-self: stretch;

        display: flex;
        justify-content: center;
        align-items: center;

        background-color: white;
        border-radius: 100px;

        font-family: 'Jost', serif;
        font-size: 48px;
        font-weight: var(--font-weight-bold);
        color: var(--color-magenta);

        opacity: 0;
        user-select: none;

        will-change: opacity, filter, transform;
        animation: fadeIn 0.3s ease-out forwards;
    }

    .buyButtonWrapper {
        grid-area: buy-button;

        opacity: 0;
        will-change: background-color, color, transform, box-shadow, opacity, filter;
        animation: fadeIn 0.3s ease-out forwards;
    }

    .buyButton {
        grid-area: buy-button;
        justify-self: stretch;

        display: flex;
        justify-content: center;
        align-items: center;

        height: 70px;

        background-color: white;
        border-radius: 100px;

        font-family: 'Jost', serif;
        font-size: 48px;
        font-weight: var(--font-weight-bold);
        color: var(--color-magenta);

        user-select: none;
        cursor: pointer;

        transition: background-color ease-out,
        color 0.3s ease-out,
        transform 0.3s ease-out,
        box-shadow 0.3s ease-out;

        &:hover {
            background-color: var(--color-magenta);
            color: white;
            transform: scale(1.05);
            box-shadow: 0 0 30px 15px rgba(122, 137, 220, 0.3);
        }
    }

    .productsGrid {
        grid-area: products-grid;

        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;

        gap: 50px;
    }

    .noCartItems {
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

export default function CartPage() {
    const dispatch = useAppDispatch()
    const location = useLocation()

    const [orderPaymentStatusBoxVisible, setOrderPaymentStatusBoxVisible] = useState(!!location.state?.paymentStatus)
    const { cart, loading: cartLoading } = useAppSelector(state => state.cart)
    const totalCartPrice = useAppSelector(state =>
        state.cart.cart.reduce((accumulator: number, cartItem: CartItem) =>
                accumulator + cartItem.product.price * cartItem.amount,
            0
        )
    )

    if (cartLoading)
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

            <div className="title">Корзина товаров</div>

            {
                !!cart

                    ? <div className="cart">
                        <div className="productsGrid">{
                            cart.map((cartItem: CartItem, index: number) =>
                                <CartItemCard cartItem={ cartItem } animationDelay={ 0.3 + 0.1 * index } />
                            )
                        }</div>

                        <div className="totalPrice">Сумма: { totalCartPrice }₽</div>

                        <div className="buyButtonWrapper">
                            <div className="buyButton" onClick={ () =>
                                dispatch(createOrder())
                            }>Оплатить
                            </div>
                        </div>
                    </div>

                    : <div className="noCartItems">корзина пустая</div>
            }
        </Root>
    )
}