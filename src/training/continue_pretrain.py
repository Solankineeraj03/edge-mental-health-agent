import os
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments

MODEL = os.getenv("BASE_MODEL", "internlm2/internlm2-7b")

def main():
    tok = AutoTokenizer.from_pretrained(MODEL, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL)
    ds = load_dataset("json", data_files={"train": "data/processed/domain_corpus.jsonl"})

    def tok_fn(b):
        return tok(b["text"], truncation=True, max_length=2048)

    ds = ds.map(tok_fn, batched=True, remove_columns=ds["train"].column_names)

    args = TrainingArguments(
        output_dir="runs/pt",
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        learning_rate=2e-5,
        num_train_epochs=1,
        logging_steps=20, save_steps=500, save_total_limit=2,
        fp16=False, bf16=True,
    )
    trainer = Trainer(model=model, args=args, train_dataset=ds["train"])
    trainer.train()
    trainer.save_model("artifacts/pt")

if __name__ == "__main__":
    main()