//Open File
function open_file(clicked_id) {
    var source_destination = clicked_id.split("_")[0]
    var connection_id = clicked_id.split("_")[2];
    var type = $("input[name='" + source_destination + "_tp_" + connection_id + "']").val();
    console.log(type);
    if (["sheets", "slides"].indexOf(type) != -1) {
        if (type == "slides") {
            var file_id = $("input[name='destination_presentation_id_" + connection_id + "']").val();
        } else {
            var file_id = $("input[name='source_sheet_id_" + connection_id + "']").val()
        }
        $.ajax({
            type : "GET", 
            url: "/google-url/" + file_id, 
            dataType: 'json', 
            success: function(data) {
                window.open(data['webViewLink'], '_blank');
            }
        })
    } else {
        if (type == "powerpoint") {
            var file_path = $("input[name='destination_presentation_path_" + connection_id + "']").val();
        } else {
            var file_path = $("input[name='source_excel_path_" + connection_id + "']").val();
        }
        window.open("/open-file/" + encodeURIComponent(file_path), '_blank');
    }
}

//Checkboxes
function checkbox_init() {
    $(".checkbox_helper").each(function(index, element) {
        var input_name = $(element).attr('name');
        var input_value = $(element).val(); 
        if (input_value === "checked") {
            $("#" + input_name).parent().checkbox('set checked')
        } else {
            $("#" + input_name).parent().checkbox('set unchecked')
        }
    })

    $('.checkbox').each(function(index, element) {
        $(element).checkbox({
            onChecked: function() {
                var input_name = $(this).attr('id');
                $("input[name='" + input_name + "']").val("checked")
            },
            onUnchecked: function() {
                var input_name = $(this).attr('id');
                $("input[name='" + input_name + "']").val("unchecked")
            }
        })
    });
}

function add_connection() {
    var new_connection = $("#connection_0").clone()
    $(new_connection).appendTo($("#connections"))
    update_ids();
    checkbox_init();
}

function delete_connection(clicked_id) {
    var connection_id = clicked_id.split("_")[2]
    $("#connection_" + connection_id).remove(); 
    update_ids();
    checkbox_init();
}

function copy_connection(clicked_id) {
    var connection_id = clicked_id.split("_")[2]
    var new_connection = $("#connection_" + connection_id).clone()
    $(new_connection).appendTo($("#connections"))
    update_ids();
    checkbox_init();
}

function clear_connection(connection_id) {
    var connection = $("#connection_" + connection_id)
    $(connection).find(".iterable_name").each(function(index, element) {
        $(this).val("")
    })
}

function update_ids() {
    var connections = [];
    var all_connections = $('[id^="connection_"]')
    all_connections.each(function(connection_index, connection) {
        if (connection_index != all_connections.length - 1) {
            var old_connection_id = $(connection).attr("id").split("_")[1]

            //Update Names
            $(connection).find(".iterable_name").each(function(index, element) {
                var id = $(element).attr("name").split("_")
                var old_id = id.pop()
                id.push((connection_index + 1).toString())
                var new_id = id.join("_")
                $(element).attr("name", new_id)
            })

            //Source Title
            source_title = $(connection).find("#source_title_" + old_connection_id)
            var text = source_title.text()
            source_title.text(text.split(" ")[0] + " (" + (connection_index + 1).toString() + ")")

            //Destination Title
            destination_title = $(connection).find("#destination_title_" + old_connection_id)
            var text = destination_title.text()
            destination_title.text(text.split(" ")[0] + " (" + (connection_index + 1).toString() + ")")

            //Update IDs
            $(connection).find(".iterable_id").each(function(index, element) {
                var id = $(element).attr("id").split("_")
                var old_id = id.pop()
                id.push((connection_index + 1).toString())
                var new_id = id.join("_")
                $(element).attr("id", new_id)
            })

            $(connection).attr("id", "connection_" + (connection_index + 1).toString())
            connections.push(connection)
        }
    });
    
    $("#connections").empty()
    connections.forEach(function(connection) {
        $("#connections").append(connection)
    })
}

function update_source_destination(source_destination_id) {
    var info = source_destination_id.split("_")
    var source_destination = info[0]
    var type = info[1]
    var connection_id = info[2]
    connection = $("#" + source_destination + "_" + connection_id); 
    $.ajax({
        type : "GET", 
        url: "/" + source_destination + "/" + type, 
        dataType: 'json', 
        success: function(data) {
            element = data['data'].replace(/{{loop.index}}/gm, connection_id.toString()).replace(/{{([^}]*)}}/gm, ""); 
            formatted_element = '<div id="' + source_destination + "_" + connection_id + '">' + element + "</div>" 
            //Replace current
            $("#" + source_destination + "_" + connection_id).replaceWith(function() {
                return formatted_element
            })
            //Change title
            $("#" + source_destination + "_title_" + connection_id).text(type.replace(/^\w/, (c) => c.toUpperCase()) + " (" + connection_id + ")")
            //Clear connection
            $("#" + source_destination + "_" + connection_id).find(".iterable_name").each(function(index, element) {
                if (!$(element).attr('name').match("_tp_")) {
                    console.log($(element).attr('name'));
                    $(element).val("");
                }
            })
        }
    }) 
} 

function strFormat() {
    var args = Array.prototype.slice.call(arguments, 1);
    return arguments[0].replace(/\{(\d+)\}/g, function (match, index) {
        return args[index];
    });
}
