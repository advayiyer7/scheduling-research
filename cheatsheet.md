# Commands Cheatsheet

## Environment
```bash
conda activate scheduling-research
conda deactivate
```

## Run Scripts
```bash
python scripts/explore_saga.py
python scripts/verify_setup.py
python scripts/run_heft_example.py
python scripts/compare_schedulers.py
```

## Tests
```bash
pytest saga/tests -k "HeftScheduler" --timeout=60
pytest saga/tests -k "CpopScheduler" --timeout=60
```

## Git
```bash
git add .
git commit -m "message"
git push
```

## Jupyter
```bash
jupyter lab
```