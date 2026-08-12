/*
 * 유튜브 인페이지 재생 (lite embed)
 *
 * data-yt="<video id>" 링크를 클릭하면 그 자리에서 iframe 으로 바꿔 재생한다.
 * 페이지 로드 시에는 유튜브에 아무 요청도 보내지 않으므로(썸네일 포함)
 * 추적 쿠키가 심기지 않고 페이지도 가벼운 상태로 유지된다.
 *
 * 새 탭에서 열고 싶으면 Ctrl/Cmd/Shift 를 누른 채 클릭하거나 가운데 버튼으로 연다.
 * JS 가 꺼져 있으면 평범한 유튜브 링크로 동작한다(href 가 그대로 살아 있음).
 */
(function () {
  'use strict';

  function makePlayer(id, label) {
    var wrap = document.createElement('span');
    wrap.className = 'yt-player';

    var frame = document.createElement('iframe');
    // youtube-nocookie: 재생 전까지 추적 쿠키를 남기지 않는 도메인
    frame.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0';
    frame.title = label || 'YouTube 영상';
    frame.loading = 'lazy';
    frame.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
    frame.allowFullscreen = true;
    frame.referrerPolicy = 'strict-origin-when-cross-origin';

    var close = document.createElement('button');
    close.type = 'button';
    close.className = 'yt-close';
    close.setAttribute('aria-label', '영상 닫기');
    close.textContent = '✕ 닫기';

    wrap.appendChild(frame);
    wrap.appendChild(close);
    return { wrap: wrap, close: close };
  }

  document.addEventListener('click', function (e) {
    var link = e.target.closest ? e.target.closest('a[data-yt]') : null;
    if (!link) return;

    // 새 탭으로 여는 조작은 브라우저 기본 동작에 맡긴다
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;

    var id = link.getAttribute('data-yt');
    if (!id) return;

    e.preventDefault();

    var player = makePlayer(id, link.textContent.trim());
    link.setAttribute('hidden', '');
    link.insertAdjacentElement('afterend', player.wrap);

    player.close.addEventListener('click', function () {
      player.wrap.remove();
      link.removeAttribute('hidden');
      link.focus();
    });
  });
})();
