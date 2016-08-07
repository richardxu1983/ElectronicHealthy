$(function () {
	// tree展开

	// clickObj 触发展开的元素
	// hiddenobj 展开的元素
	// isAccording 是否手风琴特效
	function collapse(clickObj,hiddenObj,isAccording,isSub,ajaxFun) {
		var $show = $(clickObj);
		$show.on('click', function(event) {
			if(isAccording == true) {
				$show.not(this).removeClass('active');
				$show.not(this).next(hiddenObj).slideUp(200);
			}
			$(this).toggleClass('active').next(hiddenObj).slideToggle(200);
			event.preventDefault();


	// 对tree的子项的点击事件处理  采用event来进行绑定
		if(isSub){
			// if(isAccording == true) {//移除绑定在其他子项上的事件;
			// 	var hideAll = $(hiddenObj);
			// 		hideAll.off('click');
			// }
			$hide = $(this).next(hiddenObj);
			$hide.on('click', function(event) {
			var $target = $(event.target);
				if($target.is('.sidenav-hidden-li')) {
					if(!$target.is('.active')) {
					$(clickObj).next(hiddenObj).children().removeClass('active');
					$target.addClass('active');
				}
					// 执行ajax 事件;
					if(ajaxFun)
					ajaxFun($target);
				}
			event.preventDefault();
		});
	}
		});
	}

	function dropDown(clickObj) {
		$clickObj = $(clickObj);
		$clickObj.on('click', function(event) {
			var parent = $clickObj.attr('data-parent'),target = $clickObj.attr('href');
			$(this).toggleClass('active');
			var $hiddenObj = $(this).closest(parent).find(target);
				$hiddenObj.fadeIn(200);
				event.preventDefault();
				event.stopPropagation();
			$('body').on('click', function(event) {
				var $target = $(event.target);
				if($target.parents(parent).length == 0){
					$hiddenObj.fadeOut(100);
					$('body').off('click');
				}
			});
		});
	}
	// 美化文件上传表单
	// 判断表单是否为空
	function isNull(obj) {
		return !(!$(obj).val());
	}

	// 实现左边tree
	collapse(".sidenav-show",".sidenav-hidden",true,true);
	// 实现dropDown
	dropDown(".user-show");
})
