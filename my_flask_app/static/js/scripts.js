document.addEventListener('DOMContentLoaded', function() {
    const spy = document.getElementById('spy');
    let xPosition = 0;
    let yPosition = -130; // 初期位置を低く設定
    let directionX = 1; // 1 for right, -1 for left
    let directionY = 1; // 1 for bottom to top only
    const step = 8; // 移動速度
    const containerWidth = document.getElementById('animation-container').offsetWidth;
    const containerHeight = document.getElementById('animation-container').offsetHeight;
    const spyWidth = spy.offsetWidth;
    const spyHeight = spy.offsetHeight;
    let mode = 'horizontal'; // 'horizontal' or 'vertical'
    let totalTraveledDistance = 0; // 累計移動距離
    const totalDistanceLimit = 850; // 消えるまでの総移動距離
    const switchDistance = 650; // modeを変更する距離の閾値
    let modeDistance = 0; // 現在のモードでの移動距離

    function animate() {
        // 累計距離が制限を超えたら非表示
        if (totalTraveledDistance >= totalDistanceLimit) {
            spy.style.display = 'none';
            return;
        }

        // アニメーション動作
        if (mode === 'horizontal') {
            xPosition += step * directionX;
            modeDistance += step;
            totalTraveledDistance += step;

            // 横モードの切り替え
            if (modeDistance >= switchDistance) {
                mode = 'vertical';
                modeDistance = 0; // 現在のモードでの距離をリセット
                directionY = 1; // 縦方向は上向きに
            }

            // コンテナの端で反転
            if (xPosition + spyWidth > containerWidth || xPosition < 0) {
                directionX *= -1;
                spy.style.transform = `scaleX(${directionX})`; // 画像を水平反転
            }
        } else if (mode === 'vertical') {
            yPosition += step * directionY;
            modeDistance += step;
            totalTraveledDistance += step;

            // 縦モードの切り替え
            if (modeDistance >= switchDistance) {
                mode = 'horizontal';
                modeDistance = 0; // 現在のモードでの距離をリセット
                directionX *= -1;
                spy.style.transform = `scaleX(${directionX})`;
            }

            // コンテナの上端または下端で反転
            if (yPosition + spyHeight >= containerHeight) {
                directionY = -1; // 下に移動
            } else if (yPosition <= 0) {
                directionY = 1; // 上に移動
            }
        }

        // 要素の位置更新
        spy.style.left = `${xPosition}px`;
        spy.style.bottom = `${yPosition}px`;

        // 次のアニメーションフレームをリクエスト
        requestAnimationFrame(animate);
    }

    animate();
});