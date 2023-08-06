# multitrim

Author: Kenji Gerhardt
Email: Kenji.Gerhardt@gmail.com
Github: https://github.com/KGerhardt/multitrim
User Manual: https://docs.google.com/document/d/13Oiu5UH6UTZ8lZWgO34ehj-wwZRVKwdVipqdh_qAiLE/edit?usp=sharing


Multitrim is a pipeline for Illumina short read trimming and quality control.

Multitrim accepts both single-end and paired-end reads and does the following:

1. Subsamples up to 100k reads from each read file
2. Detects adapter presence in the subsample(s) and records the sufficiently present adapter sequences by Illumina kit
3. Trims input reads with FaQCs and detected adapters
4. Retrims the FaQCs output with fastp and detected adapters
5. Uses Falco to create FastQC-like quality reports for pre-trim and post-trim reads

