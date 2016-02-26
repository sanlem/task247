function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
            	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            	break;
            }
        }
    }
    return cookieValue;
};

var getComments = function(page){
	var url = apiUrl + '?ticket=' + ticketId
	if(!page){
		page = 'last';
	} else {
		page = page.toString();
	};
	url += '&page=' + page;
	/*if(newest){
		url += '&newer_than=' + ne
		west.toString();
	};*/
	$.get(url, function(data, status){
		renderComments(data);
		addPaginationNav(data, page);
	}).fail(function(){
		// get last page if fail
		getComments();
	});

};

var addPaginationNav = function(data, page){
	var currentCount = data['results'].length;
	var count = parseInt(data['count']);
	var pages = $('#pages');
	pagesCount = Math.ceil((count - (count % pageSize)) / pageSize) + Math.ceil((count % pageSize) / pageSize);
	$('li.page').remove();
	// disable previous links if nessecary
	if(!page || page == 'last'){
		currentPage = pagesCount;
	} else {
		currentPage = page;
	};
	for(var i = 1; i <= pagesCount; i++){
		var li = $('<li/>').addClass('page');
		if(i == currentPage){
			li.addClass('active');
		};
		var a = $('<a/>', {
			'class': 'pageLink'
		}).html(i).appendTo(li);
		li.appendTo(pages);
	};

	$('.pageLink').click(function(){
		var newPage = $(this).html();
		if(newPage != currentPage){
			$('.page').removeClass('active');
			$(this).parent().addClass('active');
			getComments(newPage);
		};
	});
};

var deleteComment = function(id){
	var url = apiUrl + id.toString();
	$.ajax({
		type: "DELETE",
		url: url,
		beforeSend: function(xhr) {
			xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
		},
		success: function() {
			getComments(currentPage);
		},
	});
};

var renderComments = function(data){
	// first get the last comments' page
	$('.comment').remove();
	var amount = data['count'];
	var comments = $('#comments');
	data['results'].forEach(function(obj){
		var row = $('<article/>', {
			'class': 'row comment'
		}).appendTo(comments);
		var panel = $('<div/>', {
			'class': 'panel panel-primary'
		}).appendTo(row);
		var heading = $('<div/>', {
			'class': 'panel-heading'
		}).appendTo(panel);
		$('<h3/>', {
			'class': 'panel-title'
		}).html(obj.author).appendTo(heading);
		var body = $('<div/>', {
			'class': 'panel-body'
		}).appendTo(panel);
		$('<p/>', {
			'class': 'text comment-text'
		}).html(obj.text.replace(/\r\n|\n|\r/gm, '<br />')).appendTo(body);
		if(user == obj.author){
			$('<button/>', {
				'type': 'button',
				'class': 'btn btn-default pull-right deleteable',
				'id': obj.id
			}).html('Видалити').appendTo(heading);
		};
	});
	$('.deleteable').click(function(){
		deleteComment(parseInt($(this).attr('id')));
	});
};

var handleComments = function(){
	// ajax polling, update only current page and pagination nav
	getComments(currentPage);
};

$(document).ready(function(){
	getComments();
	// data = JSON.parse(localStorage.getItem('data'));
	var msg = $('#message');
	var msgContainer = $('#messages');
	msgContainer.hide();
	newestId = 0;
	$('#commentSubmit').click(function(){
		var textInput = $('#id_text');
		$.ajax({
			url: apiUrl,
			type: 'post',
			data: {
				text: textInput.val(),
				ticket: ticketId,
			},
			beforeSend: function(xhr, settings) {
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			},
			dataType: 'json',
			complete: function (data, status) {

				if(status == 'error'){
					msg.text('Ублюдок, введи текст коменту!');
					msgContainer.show();

				}
				else {
					msg.text('');
					msgContainer.hide();
					getComments();
				}
				textInput.val('');
			}
		});
	});
	setInterval(handleComments, 1000);
});