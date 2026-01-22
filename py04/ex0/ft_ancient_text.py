def main() -> None:
    try:
        print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
        file = open("ancient_fragment.txt", "r")
        print("Accessing Storage Vault: ancient_fragment.txt")
        print("Connection established...\n")
        print("RECOVERED DATA:")
        print(file.read())
        file.close()
        print("\nData recovery complete. Storage unit disconnected.")
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")


if __name__ == "__main__":
    main()

# 1. test commands
# tar -xzf data-generator-tools.tar.gz
# python3 data_generator.py
# python3 ft_ancient_text.py
# rm ancient_fragment.txt
# python3 ft_ancient_text.py
# 2. some terms
# storage vault	文件（如 .txt）
# access vault	open()
# extract data	read()
# preserve / inscribe	write()
# disconnect / seal	close() / with 自动关闭
# 3. about with use or not use
# “Context Managers 是整个项目层面的能力要求，我在后续的
# Vault Security 和 Crisis Response 练习中系统性地使用了 with。
# 在 Exercise 0 中，我按照题目授权函数，手动管理 open 和 close，
# 是为了展示我对文件生命周期的基础理解。”
