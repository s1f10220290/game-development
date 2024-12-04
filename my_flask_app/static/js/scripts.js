document.addEventListener('DOMContentLoaded', function () {
    const spy = document.getElementById('spy');
    const stageButton = document.getElementById('stage-button');
    const container = document.getElementById('animation-container');

    // 左端からスタートするための初期位置（%）
    let xPercent = 0; // 横方向の開始位置を左端に（0%）
    let yPercent = -28; // 縦方向の開始位置を中央に（50%）
    let directionX = 1; // 横方向の移動 (1: 右, -1: 左)
    let directionY = 1; // 縦方向の移動 (1: 上, -1: 下)
    const stepPercent = 0.5; // 移動速度（%）
    let mode = 'horizontal'; // 'horizontal' or 'vertical'
    let totalTraveledDistance = 0; // 累計移動距離（%）
    const totalDistanceLimit = 80; // 消えるまでの総移動距離（%）
    const switchDistance = 43; // モードを変更する距離の閾値（%）
    let modeDistance = 0; // 現在のモードでの移動距離
    let isReversing = false; // 反転処理中のフラグ

    function updateSpyPosition() {
        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;

        // 相対的な位置をピクセルに変換
        const xPixel = (xPercent / 100) * containerWidth;
        const yPixel = (yPercent / 100) * containerHeight;

        // スパイの位置を更新
        spy.style.left = `${xPixel}px`;
        spy.style.bottom = `${yPixel}px`;
    }

    function animate() {
        if (totalTraveledDistance >= totalDistanceLimit) {
            spy.style.display = 'none';

            // ボタンを表示
            stageButton.style.display = 'inline-block';
            return;
        }

        // アニメーション動作
        if (mode === 'horizontal') {
            xPercent += stepPercent * directionX;
            totalTraveledDistance += stepPercent;

            // 横モードの切り替え
            if (xPercent >= 43) {
                mode = 'vertical';
                modeDistance = 0; // 現在のモードでの距離をリセット
                directionY = -1; // 縦方向は上向きにするために-1
            }

            // コンテナの端で反転
            if (xPercent > 100 || xPercent < 0) {
                if (!isReversing) {
                    directionX *= -1;
                    spy.style.transform = `scaleX(${directionX})`; // 画像を水平反転
                    isReversing = true;
                }
            } else {
                isReversing = false;
            }
        } else if (mode === 'vertical') {
            yPercent += stepPercent * directionY;
            modeDistance += stepPercent;
            totalTraveledDistance += stepPercent;

            // 縦モードの切り替え
            if (modeDistance >= switchDistance) {
                mode = 'horizontal';
                modeDistance = 0; // 現在のモードでの距離をリセット
                directionX *= -1;
                spy.style.transform = `scaleX(${directionX})`;
            }

            // コンテナの端で反転
            if (yPercent > 100 || yPercent < 0) {
                if (!isReversing) {
                    directionY *= -1; // 上下方向を反転
                    isReversing = true;
                }
            } else {
                isReversing = false;
            }
        }

        // スパイの位置を更新
        updateSpyPosition();

        // 次のアニメーションフレームをリクエスト
        requestAnimationFrame(animate);
    }

    animate();
});
