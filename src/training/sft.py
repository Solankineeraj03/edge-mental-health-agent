import os
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from src.cf_sft.augment import perturb

BASE = os.getenv("PT_CKPT", "artifacts/pt")

def format_example(ex):
    ctx = ex["sensor_prompt"]
    convo = ex["dialogue"]
    sys = open("prompts/system_therapist.md").read()
    return f"<|system|>\n{sys}\n<|user|>\n{ctx}\n\n{convo}\n<|assistant|>\n{ex['target_response']}"

def main():
    ds = load_dataset("json", data_files={"train": "data/processed/sft.jsonl", "val": "data/processed/val.jsonl"})

    cf = ds["train"].map(lambda e: perturb(e))
    ds["train"] = ds["train"].flatten_indices().concatenate(cf)

    tok = AutoTokenizer.from_pretrained(BASE, use_fast=True)
    tok.pad_token = tok.eos_token

    def tok_fn(b):
        texts = [format_example(x) for x in b]
        return tok(texts, truncation=True, max_length=2048)

    ds = ds.map(tok_fn, batched=True, remove_columns=ds["train"].column_names)

    model = AutoModelForCausalLM.from_pretrained(BASE)
    collator = DataCollatorForLanguageModeling(tok, mlm=False)

    args = TrainingArguments(
        output_dir="runs/sft",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=16,
        learning_rate=1e-5,
        num_train_epochs=2,
        bf16=True,
        evaluation_strategy="steps",
        eval_steps=500,
        logging_steps=50,
        save_steps=500,
    )

    trainer = Trainer(model=model, args=args, data_collator=collator, train_dataset=ds["train"], eval_dataset=ds["val"])
    trainer.train()
    trainer.save_model("artifacts/sft")

if __name__ == "__main__":
    main()