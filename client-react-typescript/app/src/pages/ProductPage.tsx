import styled from "styled-components";
import { useParams } from "react-router-dom";
import { useEffect } from "react";

import { useAppDispatch, useAppSelector } from "../store.ts";
import { HOST } from "../conf.ts";
import { fetchProduct } from "../slices/ProductSlice.ts";
import { addCartItem, deleteCartItem } from "../slices/CartSlice.ts";
import type { CartItem } from "../interfaces/CartItemInterface.ts";

import Loader from "../components/Loader.tsx";

const Root = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;

    .productData {
        position: relative;
        height: 600px;

        display: grid;
        grid-gap: 30px;
        grid-template-columns: 4fr 3fr 3fr;
        grid-template-rows: 100px auto 100px;
        grid-template-areas:
                "image name name"
                "image description description"
                "image price add-to-cart";
    }

    .name {
        grid-area: name;

        opacity: 0;

        animation: fadeInScale 0.3s ease-out 0.3s forwards;
        will-change: transform, opacity, filter;
    }

    .price {
        grid-area: price;

        opacity: 0;

        animation: fadeInScale 0.3s ease-out 0.5s forwards;
        will-change: transform, opacity, filter;
    }

    .name, .price, .productInCart, .addToCart {
        display: flex;
        justify-content: center;
        align-items: center;

        background-color: white;
        border-radius: 100px;

        font-size: 48px;
        font-weight: var(--font-weight-bold);
        color: var(--color-magenta);
        text-wrap: nowrap;
    }

    .image {
        grid-area: image;

        height: 600px;
        box-sizing: border-box;
        border-radius: 100px;
        overflow: hidden;

        border: 2px solid white;

        opacity: 0;

        animation: fadeInFromLeft 0.3s ease-out forwards;
        will-change: transform, opacity, filter;

        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    }

    .description {
        grid-area: description;

        display: flex;
        justify-content: center;
        align-items: center;

        padding: 20px 100px;
        opacity: 0;

        background-color: white;
        border-radius: 100px;

        font-size: var(--font-size-regular);
        color: black;

        animation: fadeInScale 0.3s ease-out 0.4s forwards;
        will-change: transform, opacity, filter;
    }

    .productInCart, .addToCart {
        font-size: 32px;
        user-select: none;

        opacity: 0;

        animation: fadeInScale 0.3s ease-out 0.6s forwards;
        will-change: background-color, color, box-shadow, transform, opacity, filter;
    }

    .addToCart {
        background-color: var(--color-magenta);
        color: white;
        cursor: pointer;

        transition: background-color 0.3s ease-out, color 0.3s ease-out, box-shadow 0.3s ease-out;

        &:hover {
            background-color: white;
            color: var(--color-magenta);
            box-shadow: 0 0 30px 15px rgba(255, 255, 255, 0.5);
        }
    }

    @keyframes fadeInFromLeft {
        from {
            transform: translateX(-20%) scale(1.2);
            opacity: 0;
            filter: blur(30px);
        }
        to {
            transform: translateX(0) scale(1);
            opacity: 1;
            filter: blur(0);
        }
    }

    @keyframes fadeInFromRight {
        from {
            transform: translateX(5%);
            opacity: 0;
            filter: blur(3px);
        }
        to {
            transform: translateX(0);
            opacity: 1;
            filter: blur(0);
        }
    }

    @keyframes fadeInScale {
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

    @keyframes rootFadeOut {
        to {
            opacity: 0;
            filter: blur(30px);
            transform: scale(2);
        }
    }
`

export default function ProductPage() {
    const dispatch = useAppDispatch()

    const { productUUID } = useParams()
    const { loading: userLoading } = useAppSelector(state => state.user)
    const { product, loading: productLoading } = useAppSelector(state => state.product)
    const cartItem: CartItem = useAppSelector(state =>
        state.cart.cart.find((item: CartItem) => item.product.id === product.id)
    )

    useEffect(() => {
        dispatch(fetchProduct(productUUID))
    }, [productUUID])

    if (userLoading || productLoading)
        return <Loader />

    return (
        <Root>
            <div className="productData">
                <div className="name">{ product?.name }</div>

                <div className="image">
                    <img src={ `${ HOST }${ product?.images?.[0] }` } alt="" />
                </div>

                <div className="price">Цена: { product?.price }₽</div>
                <div className="description">{ product?.description }</div>

                {
                    !!cartItem

                        ? <div className="productInCart" onClick={
                            () => dispatch(deleteCartItem({ cartItem }))
                        }>Товар в корзине</div>

                        : <div className="addToCart" onClick={
                            () => dispatch(addCartItem({ product }))
                        }>Добавить в корзину</div>
                }
            </div>
        </Root>
    )
}