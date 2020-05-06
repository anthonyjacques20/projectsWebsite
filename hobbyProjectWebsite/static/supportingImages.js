const checkbox = $("input[type='checkbox']");
checkbox.on("click", () => {
    $(".supportImages").toggleClass('d-none');
});