import React from "react";
import styled from "styled-components";

import ProductCardCompact from "./product-card-compact.jsx";
import { updateCartItem } from "../utils.js";
import { useUser } from "../ContextProviders.jsx";


const CartItem = ({cartItem, user, setUser, animationDelay = 0}) => {
    const Root = styled.div`
        display: flex;
        flex-direction: column;
        gap: 20px;

        opacity: 0;
        will-change: filter, opacity, transform;
        animation: ${`slideIn 0.3s ease-out ${animationDelay}s forwards`};

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

        @keyframes slideIn {
            from {
                filter: blur(30px);
                opacity: 0;
                transform: translateX(-20%);
            }
            to {
                filter: blur(0);
                opacity: 1;
                transform: translateX(0);
            }
        }
    `
    const AmountControl = styled.div`
        position: relative;

        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;

        gap: 10px;

        .decreaseAmountButton, .increaseAmountButton {
            display: flex;
            justify-content: center;
            align-items: center;

            background-color: var(--color-magenta);
            stroke: white;

            width: 35px;
            aspect-ratio: 1/1;
            border-radius: 100%;

            transition: background-color 0.3s ease-out,
            stroke 0.3s ease-out,
            box-shadow 0.3s ease-out;
            will-change: background-color, stroke, box-shadow;

            &:hover {
                background-color: white;
                stroke: var(--color-magenta);
                box-shadow: 0 0 30px 15px rgba(255, 255, 255, 0.5);
            }
        }

        .amount {
            display: flex;
            justify-content: center;
            align-items: center;

            width: 50%;
            height: 35px;

            border-radius: 100px;
            background-color: var(--color-magenta);
            user-select: none;
        }
    `

    const {refreshUser} = useUser()

    return (
        <Root>
            <ProductCardCompact product = {cartItem.product} playAnimation = {false}/>
            <AmountControl>
                <div className = 'decreaseAmountButton'
                     onClick = {async () => {
                         await updateCartItem(cartItem, cartItem.amount - 1, user, setUser)
                         await refreshUser()
                     }}>
                    <svg width = "15" height = "3" viewBox = "0 0 15 3">
                        <line x1 = "1.5" y1 = "1.5" x2 = "13.5" y2 = "1.5" strokeWidth = "3"
                              strokeLinecap = "round"/>
                    </svg>
                </div>

                <div className = 'amount'>Кол-во: {cartItem.amount} шт.</div>

                <div className = 'increaseAmountButton'
                     onClick = {async () => {
                         await updateCartItem(cartItem, cartItem.amount + 1, user, setUser)
                         await refreshUser()
                     }}>
                    <svg width = "15" height = "15" viewBox = "0 0 15 15">
                        <line x1 = "7.5" y1 = "1.5" x2 = "7.5" y2 = "13.5" strokeWidth = "3"
                              strokeLinecap = "round"/>
                        <line x1 = "1.5" y1 = "7.5" x2 = "13.5" y2 = "7.5" strokeWidth = "3"
                              strokeLinecap = "round"/>
                    </svg>
                </div>
            </AmountControl>
        </Root>
    )
}

export default CartItem