import React from "react"
import styled from 'styled-components'

import ProductCardCompact from "../components/product-card-compact.jsx";
import { useUser, useProducts } from "../ContextProviders.jsx";
import Loader from "../components/loader.jsx";

const Root = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    
    gap: 50px;
    
    .productsGrid {
        display: flex;
        flex-direction: row;
        justify-content: center;
        flex-wrap: wrap;

        gap: 50px;
    }

    .noProducts {
        display: flex;

        justify-content: center;
        align-items: center;

        font-family: 'Jost', serif;
        font-size: 48px;
        font-weight: var(--font-weight-bold);
        color: var(--color-magenta);

        width: 100%;
        min-height: 500px;
        border-radius: 100px;
        user-select: none;
    }
`

const StorePage = () => {
    const {products, loading: productsLoading} = useProducts()
    const {user, loading: userLoading} = useUser()

    if (productsLoading || userLoading)
        return <Root><Loader/></Root>

    return (
        <Root>
            {
                products.length

                ? <div className = 'productsGrid'>{
                    products.map((product, index) =>
                        <ProductCardCompact key = {product.id}
                                            product = {product}
                                            animationDelay = {0.1 * index}
                        />
                    )
                }</div>

                : <div className = 'noProducts'>Товары не найдены</div>
            }
        </Root>
    )
}

export default StorePage