$(document).ready(function () {
    $(".delete_article").click(function () {
        var article_id = $(this).attr("data-article_id")
        var user_id = $("#user_id").text()
        if (confirm("Are you Sure, you want to delete this Article?")) {
            $.ajax({
                type: "GET",
                url: "/delete_article/" + parseInt(user_id) + "/" + parseInt(article_id),
                dataType: "json",
                success: function (response) {
                    if (response["success"] == true) {
                        var test = $(".news_articles .article").length
                        if (test == 1) {
                            $(".news_articles").html("<p>No Articles</p>")
                        }
                        $("#" + article_id).remove()
                        $("#hr_" + article_id).remove()
                    }
                }
            })
        }
    })
    $("#upload_new_image").click(function () {
        $(".add_article_image").show()
    })
})

function RemoveImage(index) {
    var news_id = $(".news_id_" + index).text()
    var image_txt = $(".image_txt_" + index).text()
    var data = {"news_id": news_id, "image_txt": image_txt}
    $.ajax({
        type: "POST",
        url: "/remove_image",
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: 'json',
        success: function (response) {
            if (response["success"] == true) {
                $("." + index).remove()
            }
        }
    })
}

function delete_flash(flash) {
        $(flash).parent().remove()
    }