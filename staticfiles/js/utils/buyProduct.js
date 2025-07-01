const buyProduct = async () => {
    try {
        const response = await fetch("/cart", {
            method: "POST",
            body: {
                productId: productId,
                productSlug: productSlug
            }
        });
        const data = response.json();
        return data.message;
    } catch (error) {
        return error.message;
    }
};

export default buyProduct;