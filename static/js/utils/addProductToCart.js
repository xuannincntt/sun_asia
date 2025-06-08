const addProductToCart = async (productSlug, productId) => {
    try {
        const response = await fetch("/cart/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                productId: parseInt(productId),
                productSlug: productSlug
            })
        });
        const data = await response.json();
        console.log(data);
        return data.message;
    } catch (error) {
        return error.message;
    }
};

export default addProductToCart;