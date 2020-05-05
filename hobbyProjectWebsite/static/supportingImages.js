//Find all of the supporting image divs
const supportingImages = []
for(var i = 0; i < 10; i++){
    supportingImages.push($("#supportImageDiv" + String(i)));
}

for(var j = 0; j < supportingImages.length; j++){
    if(j < supportingImages.length - 1){
        supportingImages[j].on('input', {
            nextDiv: supportingImages[j+1]
        }, function(e) {
            console.log(e.data.nextDiv);
            if(e.target.value){
                e.data.nextDiv.removeClass('d-none');
                console.log("Removing display none class")
            }
            else{
                e.data.nextDiv.addClass('d-none');
            }
        })
    }
}

//const supportingImage1 = $("#supportImageDiv0");
const image = $("input[name='image']");

image.on('input', (e) => {
    if(e.target.value){
        supportingImages[0].removeClass('d-none');
        console.log("Removing display none class")
    }
    else{
        supportingImages[0].addClass('d-none');
    }
});