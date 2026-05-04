import styled from "styled-components";
import ProductCard from "./ProductCard.tsx";
import type { OrderItem } from "../interfaces/OrderItemInterface.ts";

interface CartItemCardProps {
    orderItem: OrderItem,
    animationDelay?: number
}

interface RootProps {
    animationDelay: number
}

const Root = styled.div<RootProps>`
    display: flex;
    flex-direction: column;
    gap: 20px;

    opacity: 0;
    will-change: filter, opacity, transform;
    animation: ${ (props: RootProps) =>
            `slideIn 0.3s ease-out ${ props.animationDelay }s forwards`
    };

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
        
        color: white;
    }
`

export default function OrderItemCard(
    {
        orderItem,
        animationDelay = 0
    }: CartItemCardProps
) {
    return (
        <Root animationDelay={ animationDelay }>
            <ProductCard product={ orderItem.product } playAnimation={ false } />

            <AmountControl>
                <div className="amount">Кол-во: { orderItem.amount } шт.</div>
            </AmountControl>
        </Root>
    )
}