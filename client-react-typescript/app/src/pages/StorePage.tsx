import styled from "styled-components";
import { useAppSelector } from "../store.ts";

const Root = styled.div`

`

export default function StorePage() {
    const { store, loading: storeLoading } = useAppSelector(state => state.store)

    return (
        <Root>
            {
                store.length

                ? <div className = 'productsGrid'>{
                    store.map((product, index) =>
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