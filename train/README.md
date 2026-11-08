# Training the EcoSort classifier

The app uses a YOLOv8 image classifier trained on the **TrashNet** dataset
(6 classes: cardboard, glass, metal, paper, plastic, trash).

You train it once in Google Colab (free GPU, ~10 minutes), then commit the
resulting weights. The app loads them from `models/ecosort.pt`.

## Steps

1. Open [Google Colab](https://colab.research.google.com/) → **File → Upload notebook** →
   upload `EcoSort_TrainTrashNet.ipynb` from this folder.
2. **Runtime → Change runtime type → GPU (T4)** → Save.
3. **Runtime → Run all.** Wait ~10 min. The last cell downloads `ecosort.pt`.
4. Move the downloaded `ecosort.pt` into this repo at `models/ecosort.pt`.
5. Commit it:
   ```bash
   git add models/ecosort.pt
   git commit -m "Add trained TrashNet classifier weights"
   git push
   ```

## Notes

- `yolov8n-cls` is the smallest classifier (~3 MB trained) — small enough to
  commit directly and fast enough for Streamlit Cloud's free CPU tier.
- The notebook prints validation accuracy and a confusion matrix. Those are the
  real numbers to cite — don't round up.
- To improve accuracy later: more epochs, `yolov8s-cls`, or data augmentation.
