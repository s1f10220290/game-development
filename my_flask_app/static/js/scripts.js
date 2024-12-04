document.addEventListener('DOMContentLoaded', function () {
    const spy = document.getElementById('spy');
    const stageButton = document.getElementById('stage-button');
    const container = document.getElementById('animation-container');

    // PNG内の座標（例えば、画像の幅が100pxで高さが100pxのときに(10, 20)から始める）
    const startXPixel = 0; // PNG内での開始X座標（ピクセル）
    const startYPixel = -23; // PNG内での開始Y座標（ピクセル）

    // 画像サイズ（仮想的な値として設定）
    const imageWidth = 100; // 画像全体の幅（ピクセル）
    const imageHeight = 100; // 画像全体の高さ（ピクセル）

    // 画像内の座標をコンテナの相対位置（%）に変換
    let xPercent = (startXPixel / imageWidth) * 100;
    let yPercent = (startYPixel / imageHeight) * 100;

    let directionX = 1; // 横方向の移動 (1: 右, -1: 左)
    let directionY = -1; // 縦方向の移動 (1: 上, -1: 下)
    const stepPercent = 0.2; // 移動速度（%）
    let mode = 'horizontal'; // 'horizontal' or 'vertical'
    let totalTraveledDistance = 0; // 累計移動距離（%）
    const totalDistanceLimit = 90; // 消えるまでの総移動距離（%）
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