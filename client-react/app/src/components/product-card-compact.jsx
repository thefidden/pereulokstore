import React from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";

import { HOSTNAME } from "../conf.js";

export default function ProductCardCompact({product, playAnimation = true, animationType = 'fadeIn', animationDelay = 0}) {
    const Root = styled.div`
        opacity: ${playAnimation ? 0 : 1};
        animation: ${playAnimation 
                     ? `${animationType} 0.3s ease-out ${animationDelay}s forwards` 
                     : 'none'};
        will-change: filter, opacity, transform;

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
    const Card = styled.div`
        box-sizing: border-box;
        width: 295px;
        height: 400px;

        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;

        background-color: #7A89DC;
        border-radius: 100px;
        padding: 10px;
        cursor: pointer;

        transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;
        will-change: transform, box-shadow;

        &:hover {
            transform: scale(1.05);
            box-shadow: 0 0 30px 15px rgba(122, 137, 220, 0.3);

            img {
                transform: scale(1.05);
            }
        }

        .imageFrame {
            width: 100%;
            height: 80%;

            border-radius: 100px;
            overflow: hidden;

            img {
                width: 100%;
                height: 100%;
                object-fit: cover;

                transition: transform 0.3s ease-out;
                will-change: transform;
            }
        }

        .name, .price {
            font-family: "Jost", serif;
            font-size: 24px;
            color: white;
            user-select: none;
        }
    `

    const navigate = useNavigate()

    return (
        <Root>
            <Card onClick = {() => navigate(`/products/${product.id}`)}>
                <div className = 'imageFrame'>
                    {product && <img src = {`${HOSTNAME}${product.images[0]}`}/>}
                </div>
                <div className = 'name'>{product.name}</div>
                <div className = 'price'>{product.price}₽</div>
            </Card>
        </Root>
    )
}