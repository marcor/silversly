$.ui.menu.prototype.refresh = function() {
		var self = this;

		// don't refresh list items that are already adapted
		var items = this.element.children("li:not(.ui-menu-item):has(a)")
			.addClass("ui-menu-item")
			.attr("role", "menuitem");
		
		items.children("a")
			.addClass("ui-corner-all")
			.attr("tabindex", -1)
			// mouseenter doesn't work with event delegation
			.click(function( event ) {
                if (self.active && self.active[0] == $(this).parent()[0]) {
                    self.select(event);
                }
				else {
                    event.preventDefault();
                    event.stopPropagation();
                    self.activate( event, $(this).parent() );
                }
			});
	}
    
$.ui.menu.prototype._create = function() {
		var self = this;
		this.element
			.addClass("ui-menu ui-widget ui-widget-content ui-corner-all")
			.attr({
				role: "listbox",
				"aria-activedescendant": "ui-active-menuitem"
			});/*
			.click(function( event ) {
				if ( !$( event.target ).closest( ".ui-menu-item a" ).length ) {
					return;
				}
				// temporary
				event.preventDefault();
				self.select( event );
			});*/
		this.refresh();
	}

    
$.extend($.ui.autocomplete.prototype.options, 
        {
            source_url: null,
            source: function(request, response) {
                var widget = this;
                $.ajax({
                    "url": widget.options.source_url,
                    "data": {'term': request.term},
                    "dataType": "json",
                    "success": function(results) {
                        if (results.length > 0) { 
                            if (results[0].perfect_match) {
                                widget.element.trigger("showResult", results[0]);
                                response([])
                            } else {
                                response(results);
                            }
                        } else {
                            response(results);
                            widget.element.trigger("showResult");                           
                        }
                    }
                });
            },
            minLength: 3,
            search: function(event, ui) {
                $("#message").hide();
            },
            focus: function( event, ui ) {
                    // need to decouple this!!
                    $("#products").focus();
                    $(this).trigger("showResult", ui.item);
                    return false;
            },
            select: function( event, ui ) {
                    /*$( "#products" ).val( ui.item.fields.name );*/
                    if (ui.item) {
                        $(this).trigger("showResult", ui.item);
                    }
                    return false;
            }
        }
);
    
$.ui.autocomplete.prototype._renderItem = function( ul, item ) {
                return $( "<li></li>" )
                    .data( "item.autocomplete", item )
                    .append( "<a>" + item.fields.name + "<br/><span class=\"searchcode\">" + item.fields.code + "</span></a>" )
                    .appendTo( ul );
        };
    