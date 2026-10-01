import subprocess


def ejecutar_script(script):
    print("\n" + "=" * 60)
    print(f"EJECUTANDO: {script}")
    print("=" * 60)

    resultado = subprocess.run(
        ["python", f"etl/{script}"],
        check=True
    )

    return resultado


def main():
    print("\n")
    print("=" * 60)
    print("PIPELINE ETL - ECOMMERCE")
    print("=" * 60)

    ejecutar_script("extract.py")
    ejecutar_script("transform.py")
    ejecutar_script("load.py")

    print("\n" + "=" * 60)
    print("PIPELINE ETL COMPLETADO")
    print("=" * 60)


if __name__ == "__main__":
    main()
