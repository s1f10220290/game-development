document.addEventListener('DOMContentLoaded', function () {
    const spy = document.getElementById('spy');
    const stageButton = document.getElementById('stage-button'); // ボタンを取得

    let xPercent = 0; // 横方向の位置（%）
    let yPercent = -24; // 縦方向の位置（%）
    let directionX = 1; // 横方向の移動 (1: 右, -1: 左)
    let directionY = 1; // 縦方向の移動 (1: 上, -1: 下)
    const stepPercent = 0.5; // 移動速度（%）
    let mode = 'horizontal'; // 'horizontal' or 'vertical'
    let totalTraveledDistance = 0; // 累計移動距離（%）
    const totalDistanceLimit = 70; // 消えるまでの総移動距離（%）
    const switchDistance = 43; // モードを変更する距離の閾値（%）
    let modeDistance = 0; // 現在のモードでの移動距離

    function animate() {
        // 累計距離が制限を超えたら非表示
        if (totalTraveledDistance >= totalDistanceLimit) {
            spy.style.display = 'none';

            // ボタンを表示
            stageButton.style.display = 'inline-block';
            return;
        }

        // アニメーション動作
        if (mode === 'horizontal') {
            xPercent += stepPercent * directionX;
            modeDistance += stepPercent;
            totalTraveledDistance += stepPercent;

            // 横モードの切り替え
            if (modeDistance >= switchDistance) {
                mode = 'vertical';
                modeDistance = 0; // 現在のモードでの距離をリセット
                directionY = directionY === 0 ? 1 : directionY; // 必ず縦に移動
            }

            // コンテナの端で反転
            if (xPercent >= 100) {
                directionX = -1;
                spy.style.transform = `scaleX(-1)`; // 左向きに反転
            } else if (xPercent <= 0) {
                directionX = 1;
                spy.style.transform = `scaleX(1)`; // 右向きに反転
            }
        } else if (mode === 'vertical') {
            yPercent += stepPercent * directionY;
            modeDistance += stepPercent;
            totalTraveledDistance += stepPercent;

            // 縦モードの切り替え
            if (modeDistance >= switchDistance) {
                mode = 'horizontal';
                modeDistance = 0; // 現在のモードでの距離をリセット
            }

            // コンテナの端で反転
            if (yPercent >= 100) {
                directionY = -1; // 下向きに反転
            } else if (yPercent <= 0) {
                directionY = 1; // 上向きに反転
            }
        }

        // 要素の位置を相対的に更新
        spy.style.left = `${xPercent}%`;
        spy.style.bottom = `${yPercent}%`;

        // 次のアニメーションフレームをリクエスト
        requestAnimationFrame(animate);
    }

    animate();
});