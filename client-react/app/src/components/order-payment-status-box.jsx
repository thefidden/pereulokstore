import React, { useState } from "react";
import styled from "styled-components";

const Root = styled.div`
    position: fixed;

    display: flex;
    align-items: center;
    justify-content: center;

    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 20;

    background-color: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(3px);
    opacity: 0;

    will-change: opacity, transform, filter;
    animation: ${props =>
            props.closingAnimation
            ? 'fadeOut 0.3s ease-out forwards'
            : 'fadeIn 0.2s ease-out forwards'
    };

    @keyframes fadeIn {
        to {
            opacity: 1;
        }
    }

    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: scale(1);
            filter: blur(0);
        }
        to {
            opacity: 0;
            transform: scale(1.2);
            filter: blur(30px);
        }
    }
`
const Box = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    z-index: 22;

    box-sizing: border-box;
    padding: 100px 200px;
    gap: 50px;

    background-color: white;
    border-radius: 100px;

    font-family: 'Jost', serif;
    text-wrap: nowrap;
    box-shadow: ${props =>
            props.paymentStatus === 'successful'
            ? '0 0 50px 15px rgba(46, 158, 111, 0.5)'
            : '0 0 50px 15px rgba(214, 69, 80, 0.5)'
    };

    opacity: 0;
    user-select: none;

    will-change: opacity, transform, filter;
    animation: ${props =>
            props.closingAnimation
            ? 'fadeInBox 0.3s ease-out forwards'
            : 'fadeInBox 0.4s ease-out forwards'
    };

    .title {
        font-size: 48px;
        font-weight: var(--font-weight-bold);
        color: ${props =>
                props.paymentStatus === 'successful'
                ? 'var(--color-green)'
                : 'var(--color-red)'
        };
    }

    .description {
        font-size: 32px;
        color: ${props =>
                props.paymentStatus === 'successful'
                ? 'var(--color-green)'
                : 'var(--color-red)'
        };
    }

    .closeButton {
        position: absolute;

        z-index: 21;

        display: flex;
        justify-content: center;
        align-items: center;

        box-sizing: border-box;
        padding: 20px 50px;

        background-color: var(--color-magenta);
        border-radius: 100px;

        font-family: 'Jost', serif;
        font-size: 32px;
        font-weight: var(--font-weight-bold);
        color: white;

        user-select: none;
        cursor: pointer;
        opacity: 0;

        will-change: transform, box-shadow, opacity, filter;
        transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;
        animation: slideInCloseButton 0.3s ease-out 0.3s forwards;

        &:hover {
            transform: scale(1.05);
            box-shadow: 0 0 30px 15px rgba(122, 137, 220, 0.3);
        }

        @keyframes slideInCloseButton {
            from {
                opacity: 0;
                bottom: -100px;
                filter: blur(30px);
            }
            to {
                opacity: 1;
                bottom: -150px;
                filter: blur(0);
            }
        }
    }

    @keyframes fadeInBox {
        from {
            opacity: 0;
            transform: scale(1.2);
            filter: blur(30px);
        }
        to {
            opacity: 1;
            transform: scale(1);
            filter: blur(0);
        }
    }
`

const OrderPaymentStatusBox = ({orderId, paymentStatus, setBoxVisible}) => {
    const [closingAnimation, setClosingAnimation] = useState(false)

    async function onClose() {
        setClosingAnimation(true)
        setTimeout(() => setBoxVisible(false), 300)
    }

    return (
        <Root closingAnimation = {closingAnimation}>
            <Box paymentStatus = {paymentStatus} closingAnimation = {closingAnimation}>
                <div className = 'title'>Заказ {orderId.toUpperCase()}</div>
                <div className = 'description'>{
                    paymentStatus === 'successful'
                    ? 'Заказ успешно создан'
                    : paymentStatus === 'failure'
                      ? 'Ошибка создания заказа'
                      : ''
                }</div>
                <div className = 'closeButton' onClick = {onClose}>ОК</div>
            </Box>
        </Root>
    )
}

export default OrderPaymentStatusBox