import React from "react";
import styled from 'styled-components'

import { HOSTNAME } from "../conf.js";
import { useUser, useProduct } from "../ContextProviders.jsx";
import { userHasProductInCart, addProductToCart } from "../utils.js";
import Loader from "../components/loader.jsx";


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

const ProductPage = () => {
    const {user, loading: userLoading, refreshUser} = useUser()
    const {product, loading: productLoading} = useProduct()

    async function addToCartButtonClicked() {
        await addProductToCart(product)
        await refreshUser()
    }

    if (userLoading || productLoading)
        return <Root><Loader/></Root>

    return (
        <Root>
            <div className = 'productData'>
                <div className = 'name'>{product?.name}</div>

                <div className = 'image'>
                    <img src = {`${HOSTNAME}${product?.images?.[0]}`}/>
                </div>

                <div className = 'price'>Цена: {product?.price}₽</div>
                <div className = 'description'>{product?.description}</div>

                {
                    user !== null
                    ? userHasProductInCart(user, product)
                      ? <div className = 'productInCart'>Товар в корзине</div>
                      : <div className = 'addToCart' onClick = {addToCartButtonClicked}>Добавить в корзину</div>
                    : <></>
                }
            </div>
        </Root>
    )
}

export default ProductPage